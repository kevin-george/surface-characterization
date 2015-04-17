/********************************************************************************/
//		*** SERVOCONTROL.C ***
//	
// Control of servo movement
// 
// Author: Kevin George
//
// Requirements: The Maestro's serial mode must be set to "USB Dual Port" 
/********************************************************************************/
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <errno.h>
#include <stdlib.h>

void die(const char *message) {
  if(errno) {
    perror(message);
  } else {
    printf("\nERROR: %s\n", message);
  }
  exit(EXIT_FAILURE);
}

//Gets the position of a Maestro channel.
int getPosition(int fd, unsigned char channel) {
  unsigned char command[] = {0x90, channel};
  if(write(fd, command, sizeof(command)) == -1) {
    die("Unable to write to get response");
  }
  unsigned char response[2];
  if(read(fd,response,2) != 2) {
    die("Unable to read response");
  }
  return response[0] + (256 * response[1]);
}

//Sets the target of a Maestro channel.
//The units of 'target' are quarter-microseconds.
int setTarget(int fd, unsigned char channel, unsigned short target) {
  //Setting the protocol to be used in communication(Compact in this case)
  unsigned char command[] = {0x84, channel, target & 0x7F, target >> 7 & 0x7F};
  if(write(fd, command, sizeof(command)) == -1) {
    die("Unable to set protocol");
  }
  return 0;
}

int main() {
  //Open the Maestro's virtual COM port.
  const char* device = "/dev/ttyACM0";
  int fd = open(device, O_RDWR);
  if(fd == -1) {
    die(device);
    return 1;
  }

  int position = getPosition(fd, 0);
  printf("\nCurrent position is %d.", position);

  int target = (position < 6000) ? 7000 : 5000;
  printf("\nSetting target to %d (%d us).\n", target, target/4);
  setTarget(fd, 0, target);

  close(fd);
  return EXIT_SUCCESS;
}
