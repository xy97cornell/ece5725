/*
 test_rt.c
 11/01/18 
 Lab 04
 Xiaoyu Yan (xy97) and Ji Wu (jw2473)

 Modified rt_test file from Prof. Skovira's test_rt_skel_v6.c
*/

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>
#include <wiringPi.h>

#define MY_PRIORITY (49) /* we use 49 as the PRREMPT_RT use 50
                            as the priority of kernel tasklets
                            and interrupt handler by default */

#define MAX_SAFE_STACK (8*1024) /* The maximum stack size which is
                                   guaranteed safe to access without
                                   faulting */

#define NSEC_PER_SEC    (1000000000) /* The number of nsecs per sec. */

void stack_prefault(void) {

        unsigned char dummy[MAX_SAFE_STACK];

        memset(dummy, 0, MAX_SAFE_STACK);
        return;
}

int main(int argc, char* argv[])
{
        struct timespec t;
        struct sched_param param;
        //int interval = 50000; /* 50us*/
        int interval = 500000000; /* 0.5 sec */
        int PinValue = 0;  // used to toggle output pin
        float freq;
        int i;

        int current_sec, start_sec;

       if ( argc>=2 && atoi(argv[1] ) >0 ) { // if positive argument
          interval = atoi(argv[1]);
       }
       printf ( "Interval = %d ns\n", interval);
       //printf ( "Temp = %0.10f \n",(double) 1 / (2 * (interval) )  );
       freq = NSEC_PER_SEC * ( ( 1/(float) (2*interval) ) );
       printf ( "Frequency = %f Hz\n", freq );

        wiringPiSetup();   // initialize WiringPi
        pinMode (23, OUTPUT);  // Setup wPi pin 23 = GPIO 13 = OUTPUT

        /* Declare ourself as a real time task */
/****/
        param.sched_priority = MY_PRIORITY;
        if(sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
                perror("sched_setscheduler failed");
                exit(-1);
        }
/****/
        /* Lock memory */

        if(mlockall(MCL_CURRENT|MCL_FUTURE) == -1) {
                perror("mlockall failed");
                exit(-2);
        }

        /* Pre-fault our stack */

        stack_prefault();

        clock_gettime(CLOCK_MONOTONIC ,&t);
        /* start after one second */
        t.tv_sec++;

       printf ( "sec = %d \n", t.tv_sec);
       start_sec = t.tv_sec;
       current_sec = 0;

         while(1) {
//        while( current_sec < 5 ) {   // run the loop for 5 sec
                /* wait until next shot */
 //               clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &t, NULL);

               for ( i=0 ; i<interval ; ++i ) {  /// use delay loop to control frequency
                   // interval 1200 = about 60k Hz
               }
		
               //  code to control GPIO goes here....
		digitalWrite (23, PinValue);
		PinValue = PinValue ^ 1;
                /* calculate next shot */
                t.tv_nsec += interval;
		
                //while (t.tv_nsec >= NSEC_PER_SEC) {   // This accounts for 1 sec rollover
                //t.tv_nsec -= NSEC_PER_SEC;
                      t.tv_sec++;
                      current_sec = t.tv_sec - start_sec;  // how many seconds since we started?
                      if(current_sec > 5000000)
                      	break;
//                      //printf ( "sec = %d, current_sec = %d \n", t.tv_sec, current_sec);
                
   }
}

