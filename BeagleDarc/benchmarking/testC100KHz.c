#include <stdio.h>
#include <stddef.h>
#include <time.h>
#include <sys/time.h>
#define output "out"
#define input "in"
void delay_us(int);
int main (void)
{
    //define file handles
    FILE *ofp_export, *ofp_P8_13_value, *ofp_P8_13_direction;
    //define pin variables
    int pin_number = 23, logic_status = 1;
    char* pin_direction = output;
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d", pin_number);
    fflush(ofp_export);
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio23/direction", "w");
    if(ofp_P8_13_direction == NULL) {printf("Unable to open gpio23_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s", pin_direction);
    fflush(ofp_P8_13_direction);
    ofp_P8_13_value = fopen("/sys/class/gpio/gpio23/value", "w");
    if(ofp_P8_13_value == NULL) {printf("Unable to open gpio23_value.\n");}
    fseek(ofp_P8_13_value, 0, SEEK_SET);
    logic_status = 1;
    fprintf(ofp_P8_13_value, "%d", logic_status);
    fflush(ofp_P8_13_value);
    while(1)
    {
        //delay_us(5000);
        delay_us(5);
        logic_status = logic_status?0:1;
        //write to gpio23
        fprintf(ofp_P8_13_value, "%d", logic_status);
        fflush(ofp_P8_13_value);
    }
    fclose(ofp_export);
    fclose(ofp_P8_13_direction);
    fclose(ofp_P8_13_value);
    return 1;
}
//******************************************************************
delay_us(int desired_delay_us)
{
    struct timeval tv_start; //start time hack
    struct timeval tv_now; //current time hack
    int elapsed_time_us;
    gettimeofday(&tv_start, NULL);
    elapsed_time_us = 0;
    while(elapsed_time_us < desired_delay_us)
    {
        gettimeofday(&tv_now, NULL);
        if(tv_now.tv_usec >= tv_start.tv_usec)
            elapsed_time_us = tv_now.tv_usec - tv_start.tv_usec;
        else
            elapsed_time_us = (1000000 - tv_start.tv_usec) + tv_now.tv_usec;
        //printf("start: %ld \n", tv_start.tv_usec);
        //printf("now: %ld \n", tv_now.tv_usec);
        //printf("desired: %d \n", desired_delay_ms);
        //printf("elapsed: %d \n\n", elapsed_time_ms);
    }
}
//******************************************************************
