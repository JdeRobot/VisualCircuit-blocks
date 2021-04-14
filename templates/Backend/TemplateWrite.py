# Imporing Libraries

import numpy as np
from time import sleep
from utils.wires.wire_str import read_string, share_string
from utils.tools.freq_monitor import monitor_frequency

# Function which will be called while executing the block
def loop(block_name, input_wires, output_wires, parameters, flags):

    # Creating an output wire to write to shared memory
    output_0 = share_string(output_wires[0])

    # Checking if enable functionality is required
    # If no enable wire is present, enabled = True
    enabled = False
    try:
        enable_wire = read_string(input_wires[0])
    except IndexError:
        enabled = True

    # Setting up parameters for frequency monitoring and control
    required_frequency, update = float(parameters[0]), 1
    control_data = np.array([0.0,0.03]) # ticks, sleep_duration

    # Monitor and control freqeuncy if required.
    if flags[0] == 1:
        monitor_frequency(block_name, control_data, required_frequency, update)

    # Execute until a Keyboard interrupt is generated
    try:
    
        while True:
    
            # if no enable wire is present or check for enable/disable wire status
            if enabled or (update := bool(enable_wire.get()[0])):

                # control_data[0] contain ticks. Increments the tick count for each iteration.
                control_data[0] += 1
                            
                # Your Program Logic Goes Here
                speed_distance = [20, 10]
                
                # Convert to numpy array of specified 'U64' type.
                to_write = np.array(speed_distance, dtype='<U64')
                
                # Write array of strings to shared memory
                output_0.add(to_write)
      
            # Sleep for calculated duration to control frequency of block          
            sleep(control_data[1])
            
    # Executes when the parent process raises a Keyboard Interrupt using the console.
    except KeyboardInterrupt:

        # Release allocated memory to avoid memory leaks.
        enable_wire.release()
        output_0.release()
