#include <iostream>
#include <cv.h>
#include <highgui.h>
#include <stdlib.h>
 
using namespace std;
int main() {
  //Create window
  cvNamedWindow("Camera_Output", 1);
  
  //Capture using any camera connected to the system
  CvCapture* capture = cvCaptureFromCAM(CV_CAP_ANY);
  
  //Create image frames from capture
  IplImage* frame = cvQueryFrame(capture);     
    
  //Show image frames on created window
  cvShowImage("Camera_Output", frame);   
 
  //Release capture.
  cvReleaseCapture(&capture);  
  
  //Destroy Window
  cvDestroyWindow("Camera_Output");   
  
  return EXIT_SUCCESS;
}
