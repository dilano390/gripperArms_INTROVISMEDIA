# gripperArms_INTROVISMEDIA
The gripper arms ive made for the INTRO TO VIS MEDIA assignment


The code is centered around the gripper class. Which creates the arm based on angles given to it. The amount of arms created is based on the amount of angles given. There is no limit(within reasonable bounds)(But only the first 9 can be moved).

These angles are used to create objects of the class Section. Every frame the sections are recreated so each frame new angles can be provided. This is what allows the movement of the arms. The arm you want to move can be selected by using the numbers. This is what limits the amount of joints that can be moved.

Because I have made all of this into classes it is easy to make multiple arms using this code. I have added 2 files. One with just one arm and one with 3 arms. In this second file ive added t as a button to change between the arms.

My goal with all of this was to improve the code provided by the professor in a way that it is more object oriented. Multiple grippers can easily be made because of this more object oriented approach. Because I have isolated the core parts of the gripper into its own class(es) it can also be reused in other projects with little to no adaptation needed(You would need to port over some helper functions and probably do some other tweaks).

