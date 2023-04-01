
command_list ={
    
                # Application Commands
                # A = Application Command, C = Uses Webcam, N = No Robot Needed
    "capImg": {
        "comment": "(/300)",
        "description": " ",
        "format": " ",
        "modes": "A, C, N"
    },
        
    "recVid": {
        "comment": "(/300)",
        "description": " ",
        "format": " ",
        "modes": "A, C, N"
    },
        
    "seeText": {
        "comment": "(/300)",
        "description": " ",
        "format": " ",
        "modes": "A, C, N"
    },
        
    "": {
        "comment": "(/300)",
        "description": " ",
        "format": " ",
        "modes": "A, C"
    },
    
        
    
    
    
    
    
            # Robot Commands
    
    
    
    ";": {
        "comment": "(/098)",
        "description": "This command indicates a comment statement. These can be used throughout programs to provide documentation. A space must always follow the ; command. Although the ; statement is not an active command, it does use memory space, and slows down the operation of the robot program slightly as the comment line must be scanned just like any other. Comments should be used in a concise fashion in order to reduce both effects.",
        "format": " ; [Message]",
        "modes": "P"
    },
    
    "!": {
        "comment": "/070",
        "description": "Permits entry and modification of variable or string data. The right hand side arguments can be variable references or explicit constant values. The assigned value will be treated accordingly. Using parentheses, the mathematical expression may be expanded to provide up to 9 levels of nesting. RAPL-II provides standard built-in functions for trigonometric, mathematical, and conversion operations.",
        "format": " | <&N | VARIABLE>=<&N | 'String' | ARG1[+ | - | * | /]ARG2>",
        "modes": "I, M,P"
    },
    
    "++": {
        "comment": "(/192)",
        "description": "increment a variable by 1.",
        "format": " ++ <VARIABLENAME>",
        "modes": "I, M, P"          
    },
    
    "--": {
        "comment": "(/193)",
        "description": "Decrement a variable by 1.",
        "format": " -- <VARIABLENAME>",
        "modes": "I, M, P"
    },
    
    "ABORT": {
        "comment": "(/071)",
        "description": "Terminate existing program.",
        "format": " ABORT",
        "modes": "P"
    },
    "ACTUAL": {
        "comment": "(/152)",
        "description": "Stores the actual position of the arm.",
        "format": " ACTUAL <LOC_NAME>",
        "modes": "I, M,P"
    },
    "ALIGN": {
        "comment": "(/001)",
        "description": "Align the tool axis with the nearest major axis (X, Y or Z).",
        "format": " ALIGN",
        "modes": "I,M,P"
    },
    "ALLOC": {
        "comment": "(/018)",
        "description": "ALLOC clears and re-partitions the robot memory. This can be done with [A] Automatic or [N] Non-automatic partitioning. If [A] is selected, the memory is automatically divided according to a formula leaving 16 programs in the program table and dividing the remaining memory into 12% variable space, 38% location space and 50% program space. If [N] is used, RAPL-II prompts for the space to be allocated to the program, variable and location tables, and Path memory area. \"Reserved\" memory can also be set aside for locating user defined executable routines. This area must be partitioned by using the HIMEM command after allocating user memory.",
        "format": "ALLOC <#_PROGRAMS>, <#_VARIABLES>, <#_LOCATIONS>, <#_PATHKNOTS>",
        "modes": "I, M"
    },
    "AOUT": {
        "comment": "(/093)",
        "description": "Send a value to an analog output point ( included in the COMBO card option ). The digital value is from -5 to +5 corresponding to digital 0 to 255.",
        "format": " AOUT <OUTPUT#>,<VAR_NAME>",
        "modes": "I, M, P}"
    },
    "APPRO": {
        "comment": "(/002)",
        "description": "Move to a position a specified distance away from a user defined location. The approach path can be defined as a straight line by using the optional [,S] argument.",
        "format": " APPRO <LOC_NAME>, <DISTANCE>[,S]",
        "modes": "I, P"
    },
    "ARM": {
        "comment": "(/142)",
        "description": "Enables or disables the arm power. Can be used to turn arm power off but not back on.",
        "format": " ARM <ON | OFF>",
        "modes": "I, M, P"
    },
    "AXSTATUS": {
        "comment": "(/185)",
        "description": "Display status of each axis card.",
        "format": "[{Line#] AXSTATUS <AXIS#>,<INPUT | STATUS>,<VAR_NAME>",
        "modes": "I, M, P"
    },
    "CIRCLE": {
        "comment": "(/182)",
        "description": "Dont think this bitch has this function. Move the robot in a user defined circular path.",
    },
    "CLOSE": {
        "comment": "(/038)",
        "description": "Close the gripper. Force argument used only for optional servo gripper.",
        "format": ") CLOSE [,Force]",
        "modes": "I, P"
    },
    "CONFIG": {
        "comment": "(/110)",
        "description": "Set the configuration of one of the two serial input channels to the required baud rate, parity, etc.",
        "format": " CONFIG <DEV#>,6 <BAUD>,<PARITY>, <#DATA>, <#STOP>, <HANDSHAKE> , <ECHO>",
        "modes": "I,M,P"
    },
    "CPATH": {
        "comment": "(/163)",
        "description": "Execute a continuous path through the points specified in the argument list. Up to 16 locations can be specified. Cartesian and precision points cannot be mixed.",
        "format": " CPATH <LOC_NAME,...>",
        "modes": "I,P"
    },
    'CTPATH': {
        'comment': '/164',
        'description': 'Calculate a continuous path through a specified series of points. The points used to calculate the path must have previously been stored via Teach mode. They are identified by a template name, and a three digit number. The path is calculated using cubic-spline interpolation through the points. The path is executed using a GOPATH command.',
        "format": "[Line#)] CTPATH <PATH#>,<TEMPLATE>,<START INDEX>,<END INDEX>,<SPEED>",
        "modes": "I,P"
    },
    'CUT': {
        'comment': '/145',
        'description': 'Cut characters out of a string.',
        "format": " CUT <STR_NUM>,6 <CHAR_INDEX>, <NUM_CHARS>",
        "modes": "I,P,M"
    },
    'DECODE': {
        'comment': '/147',
        'description': 'Decode a real value from the string, starting at the character index, and load the value into the variable.',
        "format": " DECODE <STR_NUM>,<CHAR_INDEX>,<VAR_NAME>",
        "modes": "I,P,M"
    },
    'DELAY': {
        'comment': '/081',
        'description': 'Specify a time delay, in seconds. The resolution of this command is in milliseconds.',
        "format": " DELAY <TIME>",
        "modes": "I,M,P"
    },
    'DELETE': {
        'comment': '/100',
        'description': 'Delete program.',
        "format": "DELETE <PRG_NAME>",
        "modes": "I,M"
    },
    'DEPART': {
        'comment': '/004',
        'description': 'Depart from the present location (along the tool axis) by a specified amount. The optional [,S] argument will specify a straight line motion.',
        "format": " DEPART <DISTANCE>[,S]",
        "modes": "I,P"
    },
    'DEVICE': {
        'comment': '/112',
        'description': 'Select either device 0 or device 1 as the future default input/output device for user interaction.',
        "format": " DEVICE <DEV#>",
        "modes": "I,M,P"
    },
    'DIR': {
        'comment': '/102',
        'description': 'Send a list of all programs, and the corresponding memory requirements to the output device. The optional argument will send the output to the printer port.',
        "format": " DIR [1]",
        "modes": "I, M, P"
    },
    'DISABLE': {
        'comment': '/177',
        'description': 'Turn off a software feature.',
        "format": " DISABLE [Item]",
        "modes": "I.P.M "
    },
    'DLOCN': {
        'comment': '/048',
        'description': "Delete location(s) from the robot's memory.",
        "format": " DLOCN <LOC _NAME,...>",
        "modes": "I, M, P"
    },
    'DVAR': {
        'comment': '/067',
        'description': "Delete variable(s) from the robot's memory.",
        "format": " DVAR <VAR_NAME, ...>",
        "modes": "I, M, P"
    },
    'EDIT': {
        'comment': '/101',
        'description': 'Assign the specified program name for all future edit commands and enter Edit mode. The program will be created if it does not already exist.',
        "format": "EDIT [Prg_Name] ",
        "modes": "I,M"
    },
    'ELBOW': {
        'comment': '/169',
        'description': 'Specify the position of the elbow (joint #3) for future moves. Allows elimination of singularity locations.',
        "format": " ELBOW <UP | DOWN>",
        "modes": "I, P, M"  
    },
    'ENABLE': {
        'comment': '/176',
        'description': 'Turn on a software feature.',
        "format": " ENABLE [Item]",
        "modes": "I,P,M"
    },
    'ENCODE': {
        'comment': '/148',
        'description': 'Encode a value into the string, in either real or integer format.',
        "format": " ENCODE <VAR_NAME>,<STRING_NUM>{[,I]}",
        "modes": "I.P,M"
    },
    'EXECUTE': {
        'comment': '/186',
        'description': 'Causes execution of an 8086 machine language program.',
        "format": " EXECUTE <MEMORY ADDRESS>",
        "modes": "n/a"
    },
    'FINISH': {
        'comment': '/010',
        'description': 'Complete current motion command before continuing.',
        "format": "(Line#) FINISH",
        "modes": "P"        
    },
    "FLASH": {
        "comment": "/084",
        "description": "Plash the READY lamp on the Teach pendant at the specified frequency. Valid range is 1 to 255, 1 is fastest.",
        "format": " FLASH <INTERVAL>",
        "modes": "I,M,P"
    },
    "FREE": {
        "comment": "023",
        "description": "Display the current status of robot memory.",
        "format": " FREE [1]",
        "modes": "I.M,(P}"
    },
    "GAIN": {
        "comment": "/150",
        "description": "Allows the user to change the position gain of each motor servo system. A motor number of 0 will set all motors.",
        "format": "APPRO <LOC_NAME>, <DISTANCE>[,S]",
        "modes": "I, P"
    },
    "GOPATH": {
        "comment": "/165",
        "description": "Execute a path calculated with the CTPATH command.",
        "format": "[(Line#] GOPATH <PATH#>",
        "modes": "P I"
    },
    "GOSUB": {
        "comment": "/074",
        "description": "Send program control to the specified subroutine. If a list of arguments exist, then replace the current set of 8 macro parameters with the contents of the list.",
        "format": " GOSUB <PRG_NAME> [Parameter0,...,Parameter7]",
        "modes": "P"
    },
    "GOTO": {
        "comment": "/075",
        "description": "Send program control to the specified line number in the current program.",
        "format": " GOTO <LINE#>",
        "modes": "P"
    },
    "GRIP": {
        "comment": "/039",
        "description": "Commands the opening or closing of the servo gripper to a specified distance.",
        "format": " GRIP <DISTANCE>",
        "modes": "I,M,P",
    },
    "HALT": {
        "comment": "/154",
        "description": "Halt robot motion or set up a HALT ON <input#>.",
        "format": ".(Line#] HALT [ON <[-]INPUT#>]",
        "modes": "I,P"
    },
    "HELP": {
        "comment": "/095",
        "description": "Enables syntax building feature ( Help mode ).",
        "format": " HELP",
        "modes": "I,M"
    },
    "HERE": {
        "comment": "/024",
        "description": "Stores the current robot commanded position as a precision point or cartesian location in the location table.",
        "format": "(Line#)] HERE <LOC_NAME>",   
        "modes": "I,M,P"
    },
    "HIMEM": {
        "comment": "/187",
        "description": "Permits the programmer to partition a portion of the program memory for reserved use.",
        "format": "HIMEM [Buffer Size]",
        "modes": "I,P,M"
    },
    "HOME": {
        "comment": "/020",
        "description": "Send the robot to its Home position, assuming that the robot is already within bounds of the Home position. Replace the robot command registers with the calibrated Home position when it is reached.",
        "format": " HOME",
        "modes": "I,P,M"
    },
    "IF": {
        "comment": "/072",
        "description": "Evaluate the logical expression according to one of 6 operators. If the expression is true, then send program control to the specified line number.",
        "format": " IF <VARIABLE | CONSTANT> <RELATION> <VARIABLE | CONSTANT> THEN <LINE#>",
        "modes": "P",
    },
    "IFAUX": {
        "comment": "/189",
        "description": "Branch program control depending on the state of the auxiliary input.",
        "format": "{Line#] IFAUX THEN <LINE#>",
        "modes": "P"
    },
    "IFPOWER": {
        "comment": "/155",
        "description": "This a special case of IFSIG. Here the arm power status is sampled.",
        "format": " IFPOWER THEN <LINE#>",
        "modes": "P"
    },
    "IFSIG": {
        "comment": "/073",
        "description": "Examine the states of the specified inputs. If all conditions are true, then send program control to the given line number.",
        "format": " IFSIG <[-]INPUT#,...> THEN <LINE#>",
        "modes": "P",
    },
    "IFSTART": {
        "comment": "(/086)",
        "description": "Examine the state of the Auto Start button on the front panel. If it is set,then branch to the specified line number.",
        "format": "{Line#] IPSTART THEN <LINE#>",
        "modes": "P"
    },
    "IFSTRING": {
        "comment": "(/151)",
        "description": "Compare two strings and branch on result.",
        "format": " IFSTRING <&n> <== | EQ> <&n | 'TEXT'> THEN <LINE#>",
        "modes": "P"
    },
    "IGNORE": {
        "comment": "(/087)",
        "description": "Cancel ONSIG command.",
        "format": "(Line#] IGNORE",
        "modes": "I,P,M"
    },
    "INPUT": {
        "comment": "(/068)",
        "description": "Accept input from the current terminal device.",
        "format": " INPUT <VAR_NAME> | <&n>[,1]",
        "modes": "P",
    },
    "INVERT": {
        "comment": "(/170)",
        "description": "Invert the coordinate system of the robot.",
        "FORMAT": " INVERT <ON | OFF>",
        "APPLICABLE MODES": "I, M.P"
    },
    "IORD": {
        "comment": "(/085)",
        "description": "Read value of byte or word at the output port-of the 8086.",
        "format": "{Line#] IORD <BYTE | WORD>, <ADDRESS>,<VARIABLE>",
        "modes": "I, M.P"
    },
    "IOWR": {
        "comment": "(/091)",
        "description": "Write a constant or variable to the output port of 8086.",
        "format": " IOWR <BYTE | WORD>,<ADDRESS>,<VARIABLE | CONSTANT>",
        "modes": "I,M,P"
    },
    "JOG": {
        "comment": "(/005)",
        "description": "Move the robot end effector by the specified cartesian offsetsin a straight line fashion.",
        "format": " JOG <dX>,<dY>,<dZ>",
        "modes": "I, M,P"
    },
    "JOINT": {
        "comment": "(/006)",
        "description": "Move the specified joint by the given number of units.",
        "format": "{Line#] JOINT <JOINT#>,<DEGREES>",
        "modes": "I,M,(P)"
    },
    "LIMP": {
        "comment": "(/007)",
        "description": "Limp specified robot joint. No 'joint#' entered will limp all joints. Terminated by NOLIMP command.",
        "format": " LIMP [Axis#)]",
        "modes": "I,M,P"
    },
    "LISTL": {
        "comment": "(/049)",
        "description": "List all location values in a tabular format on the output device. The 1 argument will send output to the printer.",
        "format": "[Line#) LISTL [Loc_Name][,0 | 1]",
        "modes": "I,P,M"
    },
    "LISTP": {
        "comment": "(/103)",
        "description": "List the program on the output device. Send it to the printer if the 1 argument is specified.",
        "format": " LISTP <PRG_NAME>[,0 | 1]",
        "modes": "I.M,.P"
    },
    "LISTV": {
        "comment": "(/069)",
        "description": "List the variables on the output device. Send it to the printer if the 1 argument is specified.",
        "format": "(Line#] LISTV ([,0 | 1])",
        "modes": "I,M,P"
    },
    "LOCK": {
        "comment": "(/009)",
        "description": "Prevents selected joints from moving.",
        "format": "} LOCK <JOINT#,...>",
        "modes": "I, M, P"
    },
    "MA": {
        "comment": "(/132)",
        "description": "Move all 5 joints to an absolute radian position.",
        "format": " MA <j1>,<j2>»,<j3>,<j4>,<j5>",
        "modes": "I,P,M"
    },
    "MAGGRIP": {
        "comment": "(/042)",
        "description": "Adjust the magnetic strength.",
        "format": " MAGGRIP <%MAXIMUM>)",
        "modes": "I.P"
    },
    "MANUAL": {
        "comment": "(/045)",
        "description": "Activate Manual mode. The Teach pendant can be used to control robot motion either in Joint or Cylindrical mode.",
        "format": " MANUAL [JOI | CYL]",
        "modes": "I,P"
    },
    "MEMRD": {
        "comment": "(/104)",
        "description": "Read contents of a specified memory address.",
        "format": " MEMRD [Item].[Address],[Var_Name]",
        "modes": "I,P,M"
    },
    "MEMWR": {
        "comment": "(/118)",
        "description": "Write a constant or variable to a specified memory address.",
        "format": " MEMWR [Item],{Address],[Var_Name | Constant]",
        "modes": "I,P",
    },
    "MI": {
        "comment": "(/131)",
        "description": "Move all 5 joints by an incremental radian value.",
        "format": "MI <j1>,<j2>,<j3>,<j4>,<jd5>",
        "modes": "I.M, P",
    },
    "MOTOR": {
        "comment": "(/011)",
        "description": "Command an indívidual motor to move by a specified number of pulses.",
        "format": " MOTOR <MOTOR#>,<PULSES>[,INPUT PORT | ONHOME | OFFHOME]",
        "modes": "I,P,M"
    },
    "OPEN": {
        "comment": "(/040)",
        "description": "Open the gripper. Force argument used only for optional servo gripper.",
        "format": " OPEN [%FORCE]",
        "modes": "I,P",
    },
    "OUTPUT": {
        "comment": "/089",
        "description": "Set the output lines to the specified states.",
        "format": " OUTPUT <{[-]OUTPUT#,...>",
        "modes": "I, M.P",
    },
    "PASSWORD": {
        "comment": "(/141)",
        "description": "Enters Supervisory mode.",
        "format": "PASSWORD <PASSWORD>",
        "modes": "I,P,M"
    },
    "PASTE": {
        "comment": "(/146)",
        "description": "Paste string 1 into string 2, starting at the specified index.",
        "format": "_ PASTE <STRING1 | 'Text'>,<STRING2>,<CHAR_INDEX>",
        "modes": "I,P,M"
    },
    "PAUSE": {
        "comment": "(/076)",
        "description": "Pause the program flow and display the message on the output device. The program can then be continued by entering the PROCEED command.",
        "format": " PAUSE [Message String]",
        "modes": "P"
    },
    "POINT": {
        "comment": "(/050)",
        "description": "Defines a location.",
        "format": "POINT <LOC_NAME>",
        "modes": "I,M"
    },
    "PRINT": {
        "comment": "(/055)",
        "description": "Send the text string to the printer. Use a set of special characters to enhance the display. See TYPE.",
        "format": " PRINT <'text' | &n>{Argument]",
        "modes": "I, M. P",
    },
    "PRINTI": {
        "comment": "(/056)",
        "description": "Print variable(s) to the printer in an Integer format.",
        "FORMAT": "(Line#] PRINTI <VAR NAME,...>",
        "MODES": "I, M,P"
    },
    "PRINTV": {
        "comment": "(/057)",
        "description": "Print variable(s) to the printer in Real format.",
        "FORMAT": " PRINTV <VAR NAME,...>",
        "MODES": "I, M,P"
    },
    "PROCEED": {
        "comment": "(/106)",
        "description": "Continue program execution after a PAUSE command or a <Ctrl-A> has been used to halt program flow. In a program, this command will restart a path once interrupted.",
    },
    "REACH": {
        "comment": "(/171)",
        "description": "Cause to robot to access a singularity location either in forward mode ( traditional ) or by reaching 'over the head'.",
    },
    "READY": {
        "comment": "(/015)",
        "description": "Moves arm to the READY position, and any extra axes to their zero positions. Also resets any LOCK conditions.",
        "format": " READY",
        "modes": "I, M, P"
    },
    "REMOTE": {
        "comment": "(/195)",
        "description": "Enable Remote manual control from Host.",
    },
    "RENAME": {
        "comment": "(/107)",
        "description": "Rename an existing program in the robot memory.",
        "format": "RENAME <OLD PRG_NAME>,<NEW PRG_NAME>",
        "modes": "I.M"
    },
    "RETRY": {
        "comment": "(/108)",
        "description": "Retry any command which caused an error, halting program flow. That statement will be attempted again and the program will continue normally.",
    },
    "RETURN": {
        "comment": "(/077)",
        "description": "Return to calling program.",
        "format": " RETURN [Skip#]",
        "modes": "I,P,M"
    },
    "RTCLOCK": {
        "comment": "(/191)",
        "description": "Reads current state of MK48T12 real time clock.",
        "format": " RTCLOCK",
        "modes": "I,M,P"
    },
    "RUN": {
        "comment": "(/109)",
        "description": "Execute a program in memory. Execute it for a given number of cycles. Execute it only once if no loop counter is present.",
        "format": " RUN [Prg Namel[,Loop Count | F]",
        "modes": "I,P,M"
    },
    "SERIAL": {
        "comment": "(/111)",
        "description": "Display the current serial interface parameters.",
    },
    "SET":{
        "comment": "(/051)",
        "description": "Assign the value of a location to that of an existing one.",
    },
    "SHIFT": {
        "comment": "(/052)",
        "description": "Shift the cartesian displacements of a cartesían location by the specified vector.",
    },
    "SHIFTA": {
        "comment": "(/053)",
        "description": "- Shift the values of all components of the cartesían location by the specified amounts.",
    },
    "SPEED": {
        "comment": "(/016)",
        "description": "- Set the speed of future robot moves.",
    },
    "STATUS": {
        "comment": "(/025)",
        "description": "- Display the current robot status on the default output device.",
    },
    "STOP": {
        "comment": "(/078)",
        "description": "- Terminate program flow. Print the optional string on the output device.",
    },
    "STRPOS": {
        "comment": "(/149)",
        "description": "- Match the occurrence of the target string in the specified string number, and return the character index in the variable. Returns a value of zero if no match was made.",
    },
    "TEACH": {
        "comment": "(/044)",
        "description": "- Turn on the Teach mode of operatíon. Specify a Teach template which will be used to identify all future teach points. Each time the Teach button is pressed, a new location will be stored in memory. Locations can be stored according to the format described by the name; that is either a precision point or a cartesian location.",
    },
    "TIME": {
        "comment": "(/082)",
        "description": "-Extract the system timer clock value. Store the value in real format in the miven variahle",
    },
    "TOOL": {
        "comment": "(/054)",
        "description": "-Set the Tool transform to a value described by a stored 'location'.",
    },
    "TRACE": {
        "comment": "(/079)",
        "description": "- Turn on the Trace mode of operation. Each new program line which is executed will be displayed on the output device in terms of program name and line number.",
    },
    "TRIGGER": {
        "comment": "(/175)",
        "description": "- Set up a table of outputs to be turned on and/or off during path execution.",
    },
    "TYPE": {
        "comment": "(/058)",
        "description": "- Send a text string output to the default output device. Use special characters to enhance the display.",
    },
    "TYPEI": {
        "comment": "(/059)",
        "description": "-Print the list of variables to the output device in an integer format.",
    },
    "TYPEV": {
        "comment": "(/060)",
        "description": "- Print the list of variables to the output device in a real format.",
    },
    "UNLOCK": {
        "comment": "(/017)",
        "description": "- Disables LOCK command.",
    },
    "VIA": {
        "comment": "(/194)",
        "description": "- Move through a series of locations without stopping.",
    },
    "WO": {
        "comment": "/027",
        "description": "Display the current commanded robot position.",
    },
    "W1": {
        "comment": "/029",
        "description": "Display the actual robot position continuously.",
    },
    "W2": {
        "comment": "/031",
        "description": "Display the actual current robot position.",
    },
    "W3": {
        "comment": "/033",
        "description": "Displays the robot commanded position continuously on the output device.",
    },
    "W4": {
        "comment": "/035",
        "description": "Display the end coordinates of the current path.",
    },
    "W5": {
        "comment": "/037",
        "description": "Continuously displays the robot velocity command.",
        "format": " W5",
        "modes": "I,M,P"
    },
    "WAIT": {
        "comment": "/094",
        "description": "Test the condition of the input line and wait here until the condition is met.",
    },
    "WE1": {
        "comment": "/028",
        "description": "Display the actual position of the extra axes continuously.",
    },
    "WE3": {
        "comment": "/032",
        "description": "Displays the commanded position of the extra axes on the output device continuously.",
    },
    "WE5": {
        "comment": "/036",
        "description": "Displays the extra axes velocity commands continuously.",
    },
    "HLIM": {
        "comment": "/153",
        "description": "Permits numerical access to all locations stored with the same template.",
    },
    "WRIST": {
        "comment": "/172",
        "description": "Determine position of wrist for next move(s).",
    },
    "XCAL": {
        "comment": "/157",
        "description": "Calibrate an extra axis.",
    },
    "XHOME": {
        "comment": "/158",
        "description": "Home an extra axis.",
    },
    "XREADY": {
        "comment": "/014",
        "description": "Move an extra axis to its zero position.",
    },
    "XZERO": {
        "comment": "/159",
        "description": "Zero the position registers of the specified axis.",
    }
   }

    