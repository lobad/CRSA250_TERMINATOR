>>error_codes = {
    "000": "AXIS#1 OUT AXIS #1 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 1. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "001": "AXIS#2 OUT AXIS #2 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 2. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "002": "AXIS#3 OUT AXIS #3 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 3. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "003": "AXIS#4 OUT AXIS #4 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 4. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "004": "AXIS#5 OUT AXIS #5 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 5. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "005": "AXIS#6 OUT AXIS #6 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 6. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "006": "AXIS#7 OUT AXIS #7 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 7. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "007": "AXIS#8 OUT AXIS #8 IS OUT OF RANGE: This error means that there has been a Loss Of FeedBack error for joint 8. This error could be due to a collision with a stationary object, a blown fuse in the motor circuit, or a true loss of feedhack signal from the encoder.",
    "008": "ILLEGAL OPERAND: An operand in the command line is not acceptable.",
    "009": "EOL NOT FOUND: END OF LINE NOT FOUND: The end of line descriptor (a <cr>) was not found, causing an incorrect read of the data. Command lines are limited to 128 characters in length including the EOL character.",
    "010": "SYMBOL UNDEFINED: A necessary variable was not present in the symbol table. To correct, manually, or through the program logic, create a symbol in the table.",
    "011": "LOCATION UNDEFINED: The robot location referenced was not previously defined. Check the location table for the location in question, and create if necessary.",
    "012": "COMMAND ERROR: The command entered was not found in the command list. A spelling mistake, or the lack of a space between the line number and the command descriptor could have caused this problem. Either re-type the line, or inspect the program line for the mistake.",
    "013": "ARGUMENT MISSING: An argument was expected, but not read. Check the command syntax.",
    "014": "BAD SYNTAX: A general error which occurs when the command line could not be decoded. Check for a spelling error in the command name.",
    "015": "PRECISION POINT NOT LEGAL: A precision point was specified as a location in the command line, but was not permitted in this situation.",
    "016": "I/O ADDRESS ERROR: The I/O number which was entered in the command line was beyond the permissible range. Standard digital I/O is from 1 to 16, while optionally, 1 to 40 can be used.",
    "017": "PROGRAM NOT FOUND: The program called was not found in the program directory. Create the program, or check the spelling of the missing program call command.",
    "018": "ILLEGAL ARGUMENT: An argument was entered, but not permitted.",
    "019": "LINE NOT FOUND: The program line number called in a branching statement is not present in the program.",
    "020": "ARGUMENT TOO BIG",
    '021': 'NO ROOM LEFT: The program buffer is full, and cannot accept any further information. Delete unwanted programs, or re-allocate memory with the ALLOCATE command.',
    '022': 'TABLE FULL: The robot controller maintains program names, location and variable references in tables. This error means that there is no room left to store a new item. Delete all unwanted information, or re-allocate memory.',
    '023': 'BAD LINE NUMBER: The line number called could not be found, and that a value of zero was returned after its search. The value of zero is an illegal line number.',
    '024': 'ILLEGAL A/D CHANNEL: An illegal analog to digital conversion channel was specified. Channel numbers 1 to 25 are valid. Channel 9 is the speed selector knob on the teach pendant.',
    '025': 'LINE TOO LONG: The command line exceeded the maximum number of characters permitted, 128 characters.',
    '026': 'END OF FILE NOT FOUND: An end-of-file character was not found. This implies that a program buffer error has occurred. To remedy clear all memory and re-load all information. If the problem persists, then a fault exists in user memory, or a problem with storing the information on an external device caused invalid storage of information. When this information was re-loaded, the EOF character was not found, thus causing the error.',
    '027': 'PROGRAM EXISTS: An attempt to create a duplicate file name, or an attempt to load into an existing file name was discovered. Either delete the existing file, or define a new program name for the new function.',
    '028': 'LINE EXISTS: An attempt to insert an existing line number was found. Either define a new line number, or delete the old one first.',
    '029': 'TRANSFORM ILLEGAL: A move to an impossible robot coordinate was attempted and the coordinate transformation for the location generated a mathematically impossible result.',
    '032': 'JOINT #1 HOME FAILURE: The home sequence failed during the motion of axis 1. The axis was commanded a motion of just over 1000 pulses, or one motor revolution. During this motion, a zero-crossing marker pulse was expected but not seen. This could be due to an encoder failure, a wiring problem or just a lack of power to motor 1. Check for servo action and retry the HOME command. If it fails again, check encoder function and connection.',
    '033': 'JOINT #2 HOME FAILURE: Follow the same procedure as error 032.',
    '034': 'JOINT #3 HOME FAILURE: Follow the same procedure as error 032.',
    '035': 'JOINT #4 HOME FAILURE: Follow the same procedure as error 032.',
    '036': 'JOINT #5 HOME FAILURE: Follow the same procedure as error 032.',
    '037': 'JOINT #6 HOME FAILURE: Follow the same procedure as error 032.',
    '038': 'JOINT #7 HOME FAILURE: Follow the same procedure as error 032.',
    '039': 'JOINT #8 HOME FAILURE: Follow the same procedure as error 032.',
    '040': 'ARM POWER: The arm power switch was turned off, which means that no power is going to the servo motors. In this condition, the robot cannot move. The robot has been placed in a LIMP mode.',
    "041": "NOT HOMED: The robot cannot perform the requested motion because it has not been homed after power up.",
    "042": "JNT #1 OUT OF RANGE: The next motion will send joint 1 out of range. Inspect the destination point for validity.",
    "043": "JNT #2 OUT OF RANGE: Follow the same procedure as error 042.",
    "044": "JNT #3 OUT OF RANGE: Follow the same procedure as error 042.",
    "045": "JNT #4 OUT OF RANGE: Follow the same procedure as error 042.",
    "046": "JNT #5 OUT OF RANGE: Follow the same procedure as error 042.",
    "047": "CHECKSUM FAILURE: The desired item of memory (program, location or variable) has been changed in some unpredictable way. The use of this memory item could cause unexpected results. Check the item and change or edit it to the correct value.",
    "049": "MEMORY NOT ALLOCATED: RAPL-II checked user memory and believes it has not been allocated. This could be an indication of battery failure. Use the ALLOC command to partition and clear the robot memory before use.",
    "050": "AMBIGUOUS COMMAND: The user specified too few characters in a command specifier so that it is not yet a unique command choice. Re-enter the command. This error will occur when pressing a <cr> immediately after the prompt.",
    "051": "SERIAL CHANNEL #0 TIMEOUT: A timeout in serial device 0 indicating a hardware communication failure. When you see this message, the condition should already be cleared, but check the cable and its connections to be safe. If this fails, then turn system off and on.",
    "052": "SERIAL CHANNEL #0 CTS TIMEOUT: A timeout in the serial device 0 handshake control signal. This will appear only if the operator has selected a CTS/RTS handshake format. A timeout error would seem to indicate that the external device has failed, or a connection has come loose.",
    "056": "CALIBRATE CHECKSUM ERROR: The robot arm calibration values stored in memory, which are used in the homing sequence, have been corrupted. Re-Calibrate the robot or re-load the calibration values from disk using the ROBCOMM utility LOADCAL.",
    "058": "NO ACCESS: User requires supervisory access to this command. Enter the correct PASSWORD and retry the command.",
    "060": "REMOTE COMMUNICATION ERROR: Contact your distributor.",
    "062": "RET LEV NO RETURN LEVEL: Either a RETURN instruction was used when the program was not called with a GOSUB (ie. trying to RUN a subroutine), or a attempted GOSUB call would result in a subroutine nesting level greater than 10.",
    "063": "BAD AXIS N BAD AXIS NUMBER: An extra axis command was issued to a nonexistent axis. Use the @NOA command to set the number of axes.",
    "064": "NOT AVAIL NOT AVAILABLE: An option cannot be installed in the current system, or a function has been rendered unavailable with the current software.",
    "065": "SLOT USED AXIS SLOT ALREADY USED: Either the programmer was attempting to set up the controller for 8 axes while the servo or magnetic gripper option was installed, or vice versa. The programmer must deactivate the option which uses slot 8 first before assigning the new function.",
    "066": "STR ERROR STRAIGHT LINE ERROR: A straight line path was halted since it hit a joint limit. It may not be possible to move the arm out of this position using a straight line, so use a JOINT move.",
    "067": "NOT INSTAL EXPANSION MEMORY NOT INSTALLED: The continuous path command CTPATH was attempted, but the extra memory option was not installed. Could also indicate an attempt to write to a write-protected or missing EEPROM memory board.",
    "068": "N0O PATH LO MO PATH LOADED: When requesting a continuous path execution with GOPATH, the command interpreter could not find any relevant path data loaded. Re-teach the path using the CTPATH command.",
    "069": "#0 FRA ERR DEVICE 0 FRAMING ERROR: Serial device #0 framing error. A hardware communication error has been determined. Retry the communication.",
    "070": "#0 PAR ERR DEVICE 0 PARITY ERROR: Serial device #0 parity error. A hardware communication error has been determined. Retry the communication.",
    "071": "#0 OVR ERR NEVICE 0 OVERRUN ERROR: Serial device #0 overrun error. A hardware communication error has been determined. Retry the communication.",
    "072": "#1 FRA ERR DEVICE 1 FRAMING ERROR: Serial device #1 framing error. A hardware communication error has been determined. Retry the communication.",
    "073": "#1 PAR ERR DEVICE 1 PARITY ERROR: Serial device #1 parity error. A hardware communication error has been determined. Retry the communication.",
    "074": "#1 OVR ERR DEVICE 1 OVERRUN ERROR: Serial device #1 overrun error. A hardware communication error has been determined. Retry the communication.",
    "075": "UNDEF ERRO IJNDEFINED ERROR: An undefined RAPL error has been detected. This is an internal software failure which should be reported to a qualified CRS service centre.",
    "076": "IAC WRIT N IAC WRITE ERROR 1: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "077": "IAC WRIT N IAC WRITE ERROR 2: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "078": "IAC WRIT N IAC WRITE ERROR 3: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "079": "IAC WRIT N IAC WRITE ERROR 4: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "080": "IAC WRIT N IAC WRITE ERROR 5: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "081": "IAC WRIT N IAC WRITE ERROR 6: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "082": "IAC WRIT N IAC WRITE ERROR 7: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "083": "IAC WRIT N IAC WRITE ERROR 8: This error will be displayed if there has been a write error to a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "084": "IAC ERRO N IAC ERROR 1: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.", 
    "085": "IAC ERRO N IAC ERROR 2: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "086": "IAC ERRO N IAC ERROR 3: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "087": "IAC ERRO N IAC ERROR 4: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "088": "IAC ERRO N IAC ERROR 5: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "089": "IAC ERRO N IAC ERROR 6: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "090": "IAC ERRO N IAC ERROR 7: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre.",
    "091": "IAC ERRO N IAC ERROR 8: This error range will be displayed if there has been an internal error in a particular smart axis card. This error may occur during an emergency stop procedure, but should never occur during proper operation. Any occurrence of this error should be reported to a qualified CRS service centre."