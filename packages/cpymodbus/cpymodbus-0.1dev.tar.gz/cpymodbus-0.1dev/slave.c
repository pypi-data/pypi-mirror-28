/*
 * Modbus slave module.
 * Copyright sensor-sense 2017.
 * Author Jonathan Daniel.
 */

#include <Python.h>

#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <modbus.h>
#include <pthread.h>

#define _VERSION_ "0.1"

PyDoc_STRVAR(Modbus_slave_doc,
	"This module defines an object type that allows to start a modbus slave.\n"
	"Currently the module only supports RTU communication.\n"
	"The device interface is opened with R/W access. Which means the user\n"
	"must have correct access rights.");

struct server_info_s {
	modbus_mapping_t* mb_mapping; 
	modbus_t* ctx;
	pthread_t* server_thread;
	pthread_mutex_t lock;
	int8_t should_run;
};

typedef enum {
	DISCRETE_OUTPUT_COILS   = 0,
	DISCRETE_INPUT_CONTACTS = 1,
	ANALOG_INPUT_REGISTERS  = 2,
	ANALOG_OUTPUT_HOLDING_REGISTERS = 3
} register_type_t;

typedef struct server_info_s server_info_t;

/* Destructor functions for server_info_t. */
static void 
server_info_destructor(server_info_t* server_info) 
{
	modbus_mapping_free(server_info->mb_mapping);
	modbus_close(server_info->ctx);
	modbus_free(server_info->ctx);
	pthread_mutex_destroy(&(server_info->lock));
	PyMem_Free(server_info->server_thread);
	PyMem_Free(server_info);
}

static void 
Py_server_info_destructor(PyObject* obj) 
{
	server_info_t* server_info = PyCapsule_GetPointer(obj,"server_info");

	server_info_destructor(server_info);
}

/* Utility functions for server_info_t. */
static server_info_t*
PyServerInfo_AsServerInfo(PyObject* obj) 
{
	return (server_info_t *) PyCapsule_GetPointer(obj, "server_info");
}

static PyObject*
PyServerInfo_FromServerInfo(server_info_t* p, const int8_t must_free) 
{
	return PyCapsule_New(p, "server_info", must_free ? Py_server_info_destructor : NULL);
}

/* Forward declarations. */
static void*
server_loop(void* server_info);

/*
 * Check if  a register_type_t is a valid register type.
 * args:
 *	[1] register_type_t the enum.
 * return:
 *	[1] 1 if its valid 0 if not.
 */
static uint8_t 
valid_reg_type(const register_type_t reg_type)
{
	if(reg_type >= DISCRETE_OUTPUT_COILS && reg_type <= ANALOG_OUTPUT_HOLDING_REGISTERS) {
		return 1;
	}

	return 0;
}

/*
 * Get a certain bit (bit_num) from a word.
 * Returns 1 or 0.
 * args:
 *	[1] word the word to get a bit from.
 *	[2] the bit.
 */
static uint8_t 
get_bit(const int16_t word, const uint8_t bit_num)
{
	if ( bit_num <= 16) {
		return (word & (1 << (bit_num - 1)));
	}

	return 0;
}

/*
 * Write a signed int16 to a register so the master can read it.
 * Make sure when writing to a coil the maximum is 1 bit and registers are maximum 16 bit.
 * args:
  *	[1] PyCapsule pointer to server_info_t struct
 *	[2] uint address
 *	[3] int value
 *	[4] (unsigned int) register_type_t register type
 */
static PyObject*
write_register(PyObject* self, PyObject* args)
{
	uint16_t address;
	int16_t value;
	uint16_t _reg_type;
	register_type_t reg_type;
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "OHhH", &py_server_info, &address, &value, &_reg_type)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	reg_type = (register_type_t)_reg_type;
	if(!valid_reg_type(reg_type)) {
		return PyErr_SetFromErrno(PyExc_ValueError);
	}

	pthread_mutex_lock(&(server_info->lock));

	switch(reg_type) {
		case DISCRETE_OUTPUT_COILS:
			server_info->mb_mapping->tab_bits[address] = get_bit(value, 1);
			break;
		case DISCRETE_INPUT_CONTACTS:
			server_info->mb_mapping->tab_input_bits[address] = get_bit(value, 1);
			break;
		case ANALOG_INPUT_REGISTERS:
			server_info->mb_mapping->tab_input_registers[address] = value;
			break;
		case ANALOG_OUTPUT_HOLDING_REGISTERS:
			server_info->mb_mapping->tab_registers[address] = value;
			break;
	}

	pthread_mutex_unlock(&(server_info->lock));

	return Py_BuildValue("");
}

/*
 * Write an unsigned int16 to a register so the master can read it.
 * Make sure when writing to a coil the maximum is 1 bit and registers are maximum 16 bit.
 * args:
  *	[1] PyCapsule pointer to server_info_t struct
 *	[2] uint address
 *	[3] uint value
 *	[4] (unsigned int) register_type_t register type
 */
static PyObject*
unsigned_write_register(PyObject* self, PyObject* args)
{
	uint16_t address;
	uint16_t value;
	uint16_t _reg_type;
	register_type_t reg_type;
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "OHHH", &py_server_info, &address, &value, &_reg_type)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	reg_type = (register_type_t)_reg_type;
	if(!valid_reg_type(reg_type)) {
		return PyErr_SetFromErrno(PyExc_ValueError);
	}

	pthread_mutex_lock(&(server_info->lock));

	switch(reg_type) {
		case DISCRETE_OUTPUT_COILS:
			server_info->mb_mapping->tab_bits[address] = get_bit(value, 1);
			break;
		case DISCRETE_INPUT_CONTACTS:
			server_info->mb_mapping->tab_input_bits[address] = get_bit(value, 1);
			break;
		case ANALOG_INPUT_REGISTERS:
			server_info->mb_mapping->tab_input_registers[address] = value;
			break;
		case ANALOG_OUTPUT_HOLDING_REGISTERS:
			server_info->mb_mapping->tab_registers[address] = value;
			break;
	}

	pthread_mutex_unlock(&(server_info->lock));

	return Py_BuildValue("");
}

/*
 * Read out a signed value from a register.
 * args:
  *	[1] PyCapsule pointer to server_info_t struct
 *	[2] int address
 *	[3] (int) register_type_t register_type
 * return:
 *  	[1]  value  (short/int)
 */
static PyObject*
read_register(PyObject* self, PyObject* args)
{
	int address;
	register_type_t reg_type;
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "Oii", &py_server_info, &address, &reg_type)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	if(!valid_reg_type(reg_type)) {
		return  PyErr_SetFromErrno(PyExc_ValueError);
	}

	int16_t value;
	switch(reg_type) {
		case DISCRETE_OUTPUT_COILS:
			value = server_info->mb_mapping->tab_bits[address];
			break;
		case DISCRETE_INPUT_CONTACTS:
			value = server_info->mb_mapping->tab_input_bits[address];
			break;
		case ANALOG_INPUT_REGISTERS:
			value = server_info->mb_mapping->tab_input_registers[address];
			break;
		case ANALOG_OUTPUT_HOLDING_REGISTERS:
			value = server_info->mb_mapping->tab_registers[address];
			break;
	}

	return Py_BuildValue("h", value);
}

/*
 * Read out an unsigned value from a register.
 * args:
  *	[1] PyCapsule pointer to server_info_t struct
 *	[2] int address
 *	[3] (int) register_type_t register_type
 * return:
 *  	[1]  value  (ushort)
 */
static PyObject*
unsigned_read_register(PyObject* self, PyObject* args)
{
	int address;
	register_type_t reg_type;
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "Oii", &py_server_info, &address, &reg_type)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	if(!valid_reg_type(reg_type)) {
		return  PyErr_SetFromErrno(PyExc_ValueError);
	}

	uint16_t value;
	switch(reg_type) {
		case DISCRETE_OUTPUT_COILS:
			value = server_info->mb_mapping->tab_bits[address];
			break;
		case DISCRETE_INPUT_CONTACTS:
			value = server_info->mb_mapping->tab_input_bits[address];
			break;
		case ANALOG_INPUT_REGISTERS:
			value = server_info->mb_mapping->tab_input_registers[address];
			break;
		case ANALOG_OUTPUT_HOLDING_REGISTERS:
			value = server_info->mb_mapping->tab_registers[address];
			break;
	}

	return Py_BuildValue("H", value);
}

/*
 * Write to the input registers so the master can read it.
 * args:
 *	[1] PyCapsule pointer to server_info_t struct
 *	[2] int slave id
 */
static PyObject*
set_id(PyObject* self, PyObject* args)
{
	int slave;

	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "Oi", &py_server_info, &slave)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	if(modbus_set_slave(server_info->ctx, slave) == 0) {
		return Py_BuildValue("");
	} else {
		return PyErr_SetFromErrno(PyExc_RuntimeError);
	}
}

/*
 * Send the stop signal to the server, otherwise join_server_thread will block for infinity.
 * args: 
 *	[1] PyCapsule pointer to server_info_t struct
 */
static PyObject*
send_stop_signal(PyObject* self, PyObject* args)
{
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "O", &py_server_info)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	server_info->should_run = 0;

	return Py_BuildValue("");
}

/*
 * Join the server loop thread and close the connection.
 * args: 
 *	[1] PyCapsule pointer to server_info_t struct
 */
static PyObject*
join_server_thread(PyObject* self, PyObject* args)
{
	server_info_t* server_info;
	PyObject* py_server_info;

	if(!PyArg_ParseTuple(args, "O", &py_server_info)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	if(pthread_join(*(server_info->server_thread), NULL)) {
		fprintf(stderr, "Error joining thread\n");
		return PyErr_SetFromErrno(PyExc_RuntimeError);
	}

	server_info_destructor(server_info);

	return Py_BuildValue("");
}

/*
 * Set the modbus debug mode.
 * args:
 *	[1] PyCapsule containing a pointer to the server_info struct.
 *	[2] Mode, 1 or 0.
 */
static PyObject*
set_debug(PyObject* self, PyObject* args)
{
	server_info_t* server_info;
	PyObject* py_server_info;
	int8_t mode;

	if(!PyArg_ParseTuple(args, "Ob", &py_server_info, &mode)) {
		return NULL;
	}

	if(!(server_info = PyServerInfo_AsServerInfo(py_server_info))) {
		return NULL;
	}

	modbus_set_debug(server_info->ctx, mode);

	return Py_BuildValue("");
}

/*
 * This functions starts a server on another thread which must be joined with join_server thread.
 * There can currently only be one server for each python script instance.
 * args: 
 *	[1] const char* device
 *	[2] int server id
 *	[3] int baudrate
 *	[4] char parity
 *	[5] int data_bit
 *	[6] int stop_bit
 *	[7] int nb_bits
 *	[8] int nb_input_bits
 *	[9] int nb_registers
 *	[10] int nb_input_registers
 * return:
 *	[1] PyCapsule containing a pointer to the server_info struct.
 */
static PyObject*
start_server(PyObject* self, PyObject* args) 
{
	int baudrate;
	int server_id;
	int data_bit;
	int stop_bit;
	int rc;
	int nb_bits;
	int nb_input_bits;
	int nb_registers;
	int nb_input_registers;
	char parity;
	const char* dev;
	server_info_t* server_info;

	if(!PyArg_ParseTuple (
		args,
		"siiciiiiii", 
		&dev,
		&server_id,
		&baudrate, 
		&parity, 
		&data_bit, 
		&stop_bit,
		&nb_bits,
		&nb_input_bits,
		&nb_registers,
		&nb_input_registers
	)) {
		return NULL;
	}

	server_info = (server_info_t*)PyMem_Malloc(sizeof(server_info_t));
	if(server_info == NULL) {
		return PyErr_SetFromErrno(PyExc_MemoryError);
	}

	server_info->ctx = modbus_new_rtu(dev, baudrate, parity, data_bit, stop_bit);
	modbus_set_slave(server_info->ctx, server_id);

	/* Default debug mode is off. */
	modbus_set_debug(server_info->ctx, FALSE); 

	server_info->mb_mapping = modbus_mapping_new(
		nb_bits, 
		nb_input_bits,
		nb_registers,
		nb_input_registers
	); /* Init all registers  and coils. */

	if(server_info->mb_mapping == NULL) {
		modbus_free(server_info->ctx);
		return PyErr_SetFromErrno(PyExc_MemoryError);
	}

	rc = modbus_connect(server_info->ctx);

	if(rc == -1) {
		modbus_free(server_info->ctx);
		return PyErr_SetFromErrno(PyExc_RuntimeError);
	}
	server_info->should_run = 1;
	if (pthread_mutex_init(&(server_info->lock), NULL) != 0) {
		fprintf(stderr, "Error mutex init failed\n");
		return NULL;
	}

	server_info->server_thread = (pthread_t*)PyMem_Malloc(sizeof(pthread_t));
	if(pthread_create(server_info->server_thread, NULL, server_loop, (void*)server_info)) {
		fprintf(stderr, "Error creating thread\n");
		return PyErr_SetFromErrno(PyExc_RuntimeError);
	}

	return PyServerInfo_FromServerInfo(server_info, 1);
}

/*
 * This is the loop of the server thread.
 * args:
 *	[1]  pointer to server_info_t struct
 */
static void*
server_loop(void* server_info)
{
	int rc;
	uint8_t query[MODBUS_TCP_MAX_ADU_LENGTH];

	while(((server_info_t*)server_info)->should_run) {
		rc = modbus_receive(((server_info_t*)server_info)->ctx, query);
		if (rc > 0) {
			/* rc is the query size */
			modbus_reply (
				((server_info_t*)server_info)->ctx, 
				query, 
				rc, 
				((server_info_t*)server_info)->mb_mapping
			);
		} else if (rc == -1) {
			/* Connection closed by the client or error */
			//break;
		}
	}

	return NULL;
}

/* The methods to export. */
static PyMethodDef ServerMethods[] = 
{
	{"start_server", start_server, METH_VARARGS, "Start the RTU modbus server."},
	{"write_register", write_register, METH_VARARGS, "Write a signed value to a register."},
	{"unsigned_write_register", unsigned_write_register, METH_VARARGS, "Write an usnigned value to a register."},
	{"join_server_thread", join_server_thread, METH_VARARGS, "Join the server loop thread and close the server."},
	{"set_id", set_id, METH_VARARGS, "Set the slave id of the device."},
	{"set_debug", set_debug, METH_VARARGS, "Set the slave debug mode."},
	{"send_stop_signal", send_stop_signal, METH_VARARGS, "Send the stop signal to the thread."},
	{"read_register", read_register, METH_VARARGS, "Read out a signed value from a register."},
	{"unsigned_read_register", unsigned_read_register, METH_VARARGS, "Read out an unsigned value from a register"},
	{NULL, NULL, 0, NULL}
};

/* 
 * This is the modules initialisation method.
 */
PyMODINIT_FUNC
initmodbus_slave(void)
{
	Py_InitModule("modbus_slave", ServerMethods);
}