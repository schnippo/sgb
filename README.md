# sgb

smart (solar - not yet) grow box

Basic Usage:
Deploy the webserver with "python3 run.py"
Relays will be handled by the Pythondaemon "relay_daemon.py"
Sensor updates have to be handled via cron.
The PWM-Boost-Calculation ("cron_update_auto_pwm.py") aswell.
Updating the PWM is still difficult. Communication is unstable. A lot of times, the Arduino doesn't respond.
I have the following options:
        Implement it in the Relaydaemon
                Advantage: The Serialcommunication can be handled at all times via Python. (i.e. in the main while loop)
        Have it done by Cron and figure out how to get it to work.

        Key question is still:
                How should I tell the PWM-Controller which Fan to update?
                I will first set up the Pi, wire everything up and then I can debug better.
