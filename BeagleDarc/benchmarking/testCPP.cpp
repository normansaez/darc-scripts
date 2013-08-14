#include <stdio.h>
#include <stddef.h>
#include <time.h>
#define  output "out"
#define  input  "in"
int  main (void)
{
    //define file handles
    FILE *ofp_export, *ofp_P8_13_value, *ofp_P8_13_direction;
    //define pin variables
    int pin_number = 23, logic_status = 1;
    char* pin_direction = output;
    while(1){
        //establish a direction and value file within export for P8_13
        ofp_export = fopen("/sys/class/gpio/export", "w");
        if(ofp_export == NULL) {printf("Unable to open export.\n");}
        fseek(ofp_export, 0, SEEK_SET);
        fprintf(ofp_export, "%d", pin_number);
        fflush(ofp_export);
        //configure P8_13 for writing
        ofp_P8_13_direction = fopen("/sys/class/gpio/gpio23/direction", "w");
        if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
        fseek(ofp_P8_13_direction, 0, SEEK_SET);
        fprintf(ofp_P8_13_direction, "%s",  pin_direction);
        fflush(ofp_P8_13_direction);
        //write a logic 1 to P8_13 to illuminate the LED
        ofp_P8_13_value = fopen("/sys/class/gpio/gpio23/value", "w");
        if(ofp_P8_13_value == NULL) {printf("Unable to open gpio23_value.\n");}
        fseek(ofp_P8_13_value, 0, SEEK_SET);
        fprintf(ofp_P8_13_value, "%d", logic_status);
        fflush(ofp_P8_13_value);
        //close all files
        fclose(ofp_export);
        fclose(ofp_P8_13_direction);
        fclose(ofp_P8_13_value);

        logic_status = logic_status?0:1;

    }
    return 1;
}
