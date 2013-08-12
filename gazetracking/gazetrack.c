#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <dirent.h>
#include <sys/types.h>
#include "cv.h"
#include "highgui.h"
#include <X11/Xlib.h>
//#include <X11/Xutil.h>
//#include <X11/Xos.h>
#include <sys/socket.h>
#include <arpa/inet.h>
//#include <netinet/in.h>
#include <gtk/gtk.h> 

#define VID_DEV 0
#define REF_DX 9
#define REF_DY 4
#define REF_IMG_X 298
#define REF_IMG_Y 152
#define scale_factor 0.0625
#define GLINT_MIN_AREA 1
#define PUPIL_MIN_AREA 100
#define PUPIL_GLINT_MAX_DIST 25
#define True 1
#define False 0
#define CALPOINTS_X 3 // has to be >=3;
#define CALPOINTS_Y 3 // has to be >=3;
#define CALPOINT_FRAMES 100
#define ErrorMarginal 15
#define PORT 4242
#define HOST_ADDR "127.0.0.1"
#define FRAMES_POL_INTERVAL 90
#define FAILED_FRAMES_TH 60
#define SUCCEEDED_FRAMES_TH 60

#define PI 3.14159
#define min(x, y) (((x) < (y)) ? (x) : (y)) 
#define max(x, y) (((x) > (y)) ? (x) : (y))

typedef int bool; 
bool calibration=False;
bool ignoreCalibPoint=True;
bool updateTemplate=True;
bool eyeWinAbove=False;

struct size
{
    int width; 
	int height;
};

struct model
{
	float **Data;
	struct size DataSize;
};

struct calibration
{

    float **collectedDataY;
    struct size SizeY;
	float **collectedDataX;
    struct size SizeX;
	int **refPoints;
    struct size SizeRefpoints; 
	IplImage *calibImg;
	int vertical_mov;
	int horizontal_mov;
	int calibPointPos;
	int validSamples;
	int samplesNum;
    int ignoredCalibPoints;
	//calibration strating point
	CvPoint calibPoint;
};


//used in lbpcomp
IplImage *enlarged_img=0;
IplImage *block=0;
//used in glintextract
IplImage *temp=0;
IplImage *upsImg=0;
//used in radiigrad
IplImage *imgMedian=0;
CvMat *d1=0, *d1Avg=0;
//used in getReferenceTemplate
IplImage *ref_sImg=0;
IplImage *ref_lbpImg=0;
IplImage *ref_lbpImgCurrent=0;

static int Th;
static float gazeX, gazeY;

void LBP(IplImage *img, IplImage *lbpImg);
void lbpcomp(IplImage *img, IplImage *img2, CvMat *result);
int lbpcomp_block(IplImage *img, IplImage *img2);
int lbpcomp_arrays(unsigned char *a, unsigned char *b, int i);
void glintextract(IplImage *img, IplImage *img2, IplImage *resultImg);
void blobExtraction(IplImage *img, int min_blobArea, CvPoint2D32f *blobCenters, int* numBlobs);
void radiigrad(IplImage *img, CvPoint2D32f *point, CvPoint2D32f *resultPoint);
int gazevect(CvPoint2D32f *pupil, CvPoint2D32f *glints, int numGlints, CvPoint2D32f *resultGazeVect);
void match(CvPoint2D32f *gazevect, struct model *m);
void readModelDataFile(char *fileName, struct model *m);
float** allocate2DFloatArray(struct size);
void free2DFloatArray(struct size, float **array);
int** allocate2DInttArray(struct size);
void free2DIntArray(struct size, int **array); 
void writeModelDataFile(char *fileName, float **inputData, int lines);
IplImage* getReferenceTemplate(IplImage* refImg, int x, int y, int downscaleImg);
IplImage* getReferenceFrame();
void model(CvPoint2D32f *vector, float *result);
void CalculateModelData(float **dataX, float **dataY, int **refPoints, int numSamples, struct model *result);
void getScreenSize(struct size *s);
void initCalibration(struct calibration *calib, struct size *screenSize);
void updateCalibration(int frameNum, struct calibration *calib, struct model *m);
void saveCalibrationData(struct calibration *calib, CvPoint2D32f *GazeVect, struct size *screenSize);
void parseCommandline(int argc, char* argv[], struct model *m, IplImage** refImg/*, bool calib*/);
int composeMessage(int x, int y, char *message);
int filter(int data[]);
void downscale(IplImage *srcImg, IplImage *destImg);
IplImage* getImagesfromDir(int frame);
void setWindowAvove(char *winName);
void setWindowBelow(char *winName);


inline float EulerianDistance(CvPoint2D32f *point1, CvPoint2D32f* point2)
{
	return sqrt((point1->x - point2->x) * (point1->x - point2->x) + (point1->y - point2->y) * (point1->y - point2->y));
}

/*inline CvPoint ProjectToImgCoord(CvPoint2D32f *point)
{
	return cvPoint2D32f(screen_width/2+point->x, screen_hight/2+point->y);
}*/

inline CvPoint ProjectToImgCoord(float x, float y, struct size *s)
{
	return cvPoint(round(s->width/2+x), round(s->height/2+y));
}

inline CvPoint2D32f ProjectToCartesianCoord(float x, float y, struct size *s)
{
	return cvPoint2D32f(x-s->width/2, y-s->height/2);
}

inline IplImage* allocateImage(IplImage* img, CvSize size, int depth, int nChannels )
{

    if (img != NULL)
    {

        if(img->width==size.width && img->height==size.height && img->depth==depth && img->nChannels==nChannels) 
            return img;
        else
        {
            cvReleaseImage(&img);
            img = cvCreateImage(size, depth, nChannels);
            //fprintf(stderr, "image reallocated\n");
            if (img == NULL)
            {
                fprintf(stderr, "\nERROR: Couldn't allocate image...");
                exit(-1);
            }
                return img;
        }
    }

    img = cvCreateImage(size, depth, nChannels);
    //fprintf(stderr, "new image allocated\n");
    if (img == NULL)
    {
        fprintf(stderr, "\nERROR: Couldn't allocate image...");
        exit(-1);
    }

    return img;
}

inline CvMat* allocateMatrice(CvMat *mat, int rows, int cols, int type)
{

    if (mat != NULL)
    {

        if(mat->rows==rows && mat->cols==cols && mat->type==(CV_MAT_MAGIC_VAL|type|CV_MAT_CONT_FLAG)) 
            return mat;              
        else
        {
            cvReleaseMat(&mat);
            mat=cvCreateMat(rows, cols, type);
            //fprintf(stderr, "matrice reallocated\n");
            if (mat == NULL)
            {
                fprintf(stderr, "\nERROR: Couldn't allocate matrice...");
                exit(-1);
            }

            return mat;
        }
    }

    mat = cvCreateMat(rows, cols, type);
    //fprintf(stderr, "new matrice allocated\n");
    if (mat == NULL)
    {
        fprintf(stderr, "\nERROR: Couldn't allocate matrice...");
        exit(-1);
    }
    
    return mat;
}

int main( int argc, char **argv )
{

	//init globals
	Th=-1;
	gazeX=0, gazeY=0;
    int Sx = 0, Sy = 0, Px = 0, Py = 0, Kx=0, Ky=0, sradi=0, z=0;
	int xa=0, ya=0, xb=0, yb=0, i=0;
    int COST_LIMIT =(2*REF_DX-1) * (2*REF_DY-1)*2;
	int comp=0, numGlints=0, numPupils=0;
	int succeeded=0;
	int frameNum=-1;
    int failedFrames=0;
    int succeededFrames=0;
	double cost, mv, deltaX=0, deltaY=0;

    struct size screenSize;
    struct model model_;
	int sock, len;
	char buffer[100];
    struct sockaddr_in server;

	CvPoint2D32f GazeVect[4];
	CvPoint min_loc;
	CvPoint2D32f glintCenter[10], pupilCenterAprx[4];
	CvPoint2D32f pupilCenter;
	CvMat *result_Matrice=0;
	CvSize scaledSize;
	IplImage *img=0;// = cvCreateImage(size,8,1);
	IplImage *frame_lbpImg=0;
	IplImage *Ieye=0;
	IplImage *grIeye=0;
	IplImage *cropImg=0;
	IplImage *cropImg2=0;
	IplImage *IeyeBinary=0;
	IplImage *IeyeBinaryMedian=0;
	IplImage *glintsImg=0;
	IplImage *IeyeRGB=0;
	int new_height;
	int new_width;
	IplImage *sImg=0; 

    struct calibration calib;
	/*float **collectedDataY;
    struct size SizeY;
	float **collectedDataX;
    struct size SizeX;
	int **refPoints;
    struct size SizeRefpoints; 
	IplImage *calibImg=0;
	int vertical_mov=screenSize.width/(CALPOINTS_X*CALPOINTS_X-1);
	int horizontal_mov=screenSize.height/(CALPOINTS_Y*CALPOINTS_Y-1);
	int calibPointPos=1;
	int validSamples=0;
	int samplesNum=CALPOINTS_X*CALPOINTS_Y*CALPOINT_FRAMES;
	//calibration strating point
	CvPoint calibPoint=cvPoint(vertical_mov, horizontal_mov);
    int ignoredCalibPoints=0;*/
	
	
	IplImage *imgRGB=0;	
	IplImage *refImg=0;
    IplImage *template=0;

	
    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) 
	{
        fprintf (stderr,"\nERROR: opening socket");
    }

    memset(&server, 0, sizeof(server));       
    server.sin_family = AF_INET;                  
    server.sin_addr.s_addr = inet_addr(HOST_ADDR);  
    server.sin_port = htons(PORT);

	if (connect(sock, (struct sockaddr*) &server, sizeof(server)) < 0) 
	{
        fprintf (stderr,"\nERROR: unable to connect to the host");
		//exit(0);	 
    }
 
    getScreenSize(&screenSize);
	fprintf(stderr,"\nwidth: %i height: %i", screenSize.width, screenSize.height);
//--------------------------------------------------------------------------
//   Get a reference rectangle for matching
//--------------------------------------------------------------------------

    parseCommandline(argc, argv, &model_, &refImg);
    if(refImg==NULL)
        fprintf(stderr, "\nERROR: refImg is NULL");

    if(model_.Data==NULL)
        fprintf(stderr, "\nERROR: modelData is NULL");

    fprintf(stderr, "\nmodelDataLen %i\n", model_.DataSize.height);
	template = getReferenceTemplate(refImg, REF_IMG_X, REF_IMG_Y, True);
	//cvSaveImage("referenceTemplate.png", template, 0);
       
//-------------------------------------------------------------------------
//   Process input frames
//-------------------------------------------------------------------------

    CvCapture *capture = 0;
	capture = cvCaptureFromCAM(VID_DEV);

   	if (!capture) 
	{
        fprintf(stderr, "\nERROR: capture is NULL");
     	exit(1);
   	}

   	cvNamedWindow("eye", CV_WINDOW_AUTOSIZE);
    cvMoveWindow("eye", screenSize.width/2-(REF_DX/scale_factor), screenSize.height/2-(REF_DY/scale_factor));
	//char filename[15];	
	char base[8]= "capture";
	//char end[4] = ".png";
	
	if(calibration==True)
	{
        initCalibration(&calib, &screenSize);
		/*collectedDataX=malloc(samplesNum*sizeof(float*));
		collectedDataY=malloc(samplesNum*sizeof(float*));
		refPoints=malloc(samplesNum*sizeof(int*));
        //allocate2DFloatArray(collectedDataX);
		cvNamedWindow("calibration", CV_WINDOW_AUTOSIZE);
		cvMoveWindow("calibration", 0, 0);
		calibImg = cvCreateImage(cvSize(screenSize.width, screenSize.height),8,3);
		cvCircle(calibImg,calibPoint , 15, cvScalar(255,255,255,0), -1, CV_AA, 0);*/
	}

	int frameH = (int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);
	int frameW = (int) cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
	new_height = (int)(frameH*scale_factor);
	new_width =(int)(frameW*scale_factor);
	sImg = cvCreateImage(cvSize(new_width, new_height), 8, 1);
	Ieye = cvCreateImage(cvSize((int)(2*REF_DX/scale_factor), (int)(2*REF_DY/scale_factor)), 8, 1);
	IeyeRGB = cvCreateImage(cvGetSize(Ieye), Ieye->depth,3);
	glintsImg = cvCreateImage(cvGetSize(Ieye), Ieye->depth, Ieye->nChannels);
	IeyeBinary = cvCreateImage(cvGetSize(Ieye), 8, 1);
	IeyeBinaryMedian = cvCreateImage(cvGetSize(Ieye), 8, 1); 

	//cFrameNum=-1;
   	while(1) 
	{ 

		frameNum++;
		fprintf(stderr,"\nframe: %i", frameNum);

		if ((cvWaitKey(10) & 255) == 27 ) 
			break;


        if(frameNum%FRAMES_POL_INTERVAL==0 && eyeWinAbove==False)
            failedFrames=0;

        if(frameNum%FRAMES_POL_INTERVAL==0 && eyeWinAbove==True)
            succeededFrames=0;            
        

        if(failedFrames==FAILED_FRAMES_TH)
        {
            setWindowAvove("eye");
            eyeWinAbove=True;
            failedFrames=0;
            succeededFrames=0;
        }

        if(succeededFrames==SUCCEEDED_FRAMES_TH)
        {
            setWindowBelow("eye");
            eyeWinAbove=False;
            failedFrames=0;
            succeededFrames=0;
        }

		img=cvQueryFrame(capture);
                //img=getImagesfromDir(frameNum);
        
     	if (!img) 
		{
       	    fprintf(stderr, "\nERROR: frame is null...");
       		continue;
     	}

		if(calibration==True)
            updateCalibration(frameNum, &calib, &model_);
		/*{
            
			if(frameNum%CALPOINT_FRAMES==0 && frameNum!=0)
			{
				cvSetZero(calibImg);
				if(calibPointPos%CALPOINTS_X==0)
				{
					calibPoint.x=vertical_mov;
					calibPoint.y+=horizontal_mov*CALPOINTS_Y;
				}
				else
					calibPoint.x+=vertical_mov*CALPOINTS_X;
					
				calibPointPos++;
				ignoreCalibPoint=True;
				cvCircle(calibImg,calibPoint , 15, cvScalar(255,255,255,0), -1, CV_AA, 0);
			}
			
			cvShowImage("calibration", calibImg);
		
			if(calibPointPos==CALPOINTS_X*CALPOINTS_Y+1)
			{
				calibration=False;
				cvReleaseImage(&calibImg);
				cvDestroyWindow("calibration");

				//for(z=0; z<modelDataLen; z++)
				//{
				//	free(modelData[z]);
				//}
				//free(modelData);

				//modelData=CalculateModelData(collectedDataX, collectedDataY, refPoints, validSamples);
                CalculateModelData(collectedDataX, collectedDataY, refPoints, validSamples, &model_);
				//free the calibration data not needed anymore
				//for(z=0; z<validSamples; z++)
				//{
				//	free(collectedDataX[z]);
				//	free(collectedDataY[z]);
				//}
				//free(collectedDataX);
				//free(collectedDataY);
			}
		}*/
        
        downscale(img, sImg);		
        //cvResize(img, sImg, CV_INTER_LINEAR);
		scaledSize = cvGetSize(sImg);
		
		if(Sx==0)
		{
			sradi = 0;
			Sy = 1;
			Sx = 1;
			ya = 1;
			xa = 1;
			yb = scaledSize.height;
			xb = scaledSize.width;
		}
		else
		{
			Ky = max(min(Sy + floor(deltaY*0.5), scaledSize.height-1),2);
		    Kx = max(min(Sx + floor(deltaX*0.5), scaledSize.width-1),2);

			if(cost<COST_LIMIT)
				sradi=3;
			else
				sradi=10000; //just a large number
	
			ya = max(Ky-sradi-(REF_DY-1),1); 
			yb = min(Ky+sradi+(REF_DY-1), scaledSize.height);
		    xa = max(Kx-sradi-(REF_DX-1),1); 
			xb = min(Kx+sradi+(REF_DX-1), scaledSize.width);
			Py = Sy; 
			Px = Sx;
		    Sx = xa; 
			Sy = ya;	
			
		}

		cvSetImageROI(sImg, cvRect(xa, ya, xb-xa, yb-ya));
        cropImg=allocateImage(cropImg, cvGetSize(sImg), sImg->depth, 1);
		//cropImg = cvCreateImage(cvGetSize(sImg),sImg->depth,sImg->nChannels);
        //printf("\ncropImg width=%i    cropImg height=%i", cropImg->width, cropImg->height);
		cvCopy(sImg, cropImg, NULL);
		cvResetImageROI(sImg);
		//printf("\nsImg width=%i height=%i", sImg->width, sImg->height);
		//printf("\ncropImg width=%i    cropImg height=%i", cropImg->width, cropImg->height);
		//frame_lbpImg=cvCreateImage(cvGetSize(cropImg),8, 1);
        frame_lbpImg=allocateImage(frame_lbpImg, cvGetSize(cropImg),8, 1);
		LBP(cropImg, frame_lbpImg);
		//cvReleaseImage(&cropImg);

        result_Matrice=allocateMatrice(result_Matrice, frame_lbpImg->height, frame_lbpImg->width, CV_32SC1);
		//result_Matrice = cvCreateMat(frame_lbpImg->height, frame_lbpImg->width, CV_32SC1);
		lbpcomp(frame_lbpImg, template, result_Matrice);
         
		cvMinMaxLoc(result_Matrice, &cost, NULL, &min_loc, NULL, NULL);
		Sy = min(max(Sy + min_loc.y, REF_DY+1), scaledSize.height-REF_DY-1);
        Sx = min(max(Sx + min_loc.x, REF_DX+1), scaledSize.width-REF_DX-1);

//////////////////////////////////////debug print//////////////////////////////////////////////////////////
		/*int l,b;
		for (l = 0; l < result_Matrice->rows; l++)
		{
			printf("\n"); 
			for(b = 0; b < result_Matrice->cols; b++)
			{
				if(l==min_loc.y && b==min_loc.x)
					printf (" |%i|",(int)(cvGetReal2D(result_Matrice, l, b)));
				else
					printf (" %i",(int)(cvGetReal2D(result_Matrice, l, b)));
			}
		}*/
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		fprintf(stderr,"    min loc: x=%i  y=%i     cost: %i", min_loc.x, min_loc.y, (int)cost);
		//printf("\ncost:%f", cost);
		
		if(Px == 0)
		{
            deltaY = 0;
            deltaX = 0;
		}
		else
		{
			deltaY = Sy - Py;
            deltaX = Sx - Px;
		}
		//printf("\nSx: %i Sy: %i\n",Sx, Sy);

		//printf("\nimg width= %i    img height= %i   nChannels= %i\n", img->width, img->height, img->nChannels);

		cvSetImageROI(img, cvRect((int)((Sx-REF_DX)/scale_factor), (int)((Sy-REF_DY)/scale_factor), (int)(2*REF_DX/scale_factor), (int)(2*REF_DY/scale_factor)));
		cvCopy(img, Ieye, NULL);
		cvResetImageROI(img);

		cvSetImageROI(sImg, cvRect(Sx-REF_DX, Sy-REF_DY, 2*REF_DX, 2*REF_DY));
        cropImg2=allocateImage(cropImg2, cvGetSize(sImg),8,1);
		//cropImg = cvCreateImage(cvGetSize(sImg), sImg->depth, sImg->nChannels);
		cvCopy(sImg, cropImg2, NULL);
		cvResetImageROI(sImg);
		glintextract(Ieye, cropImg2, glintsImg);
		blobExtraction(glintsImg, GLINT_MIN_AREA, glintCenter, &numGlints);

        //fprintf(stderr, "\n............");
		cvCvtColor(Ieye, IeyeRGB, CV_GRAY2RGB);
		for(z=0; z<numGlints; z++)
		{
			cvLine(IeyeRGB, cvPoint(glintCenter[z].x-5, glintCenter[z].y), cvPoint(glintCenter[z].x+5, glintCenter[z].y), cvScalar(0,0,255,0), 1, CV_AA, 0);
			cvLine(IeyeRGB, cvPoint(glintCenter[z].x, glintCenter[z].y-5), cvPoint(glintCenter[z].x, glintCenter[z].y+5), cvScalar(0,0,255,0), 1, CV_AA, 0);	
		}

		if(glintCenter==NULL)
		{
			fprintf(stderr, "\nERROR: No glints...");
            if(eyeWinAbove==False)
                failedFrames++;

			continue;
		}

		if(numGlints < 4)
		{
			cvShowImage("eye", IeyeRGB);
			fprintf(stderr, "\nERROR: Not enough glints, found only %i...", numGlints);
            if(eyeWinAbove==False)
                failedFrames++;

			continue;
		}

		cvMinMaxLoc(Ieye, &mv, NULL, NULL, NULL, NULL);
		mv = mv + 15;

        cvCmpS(Ieye, mv, IeyeBinary, CV_CMP_LT);
		cvSmooth(IeyeBinary, IeyeBinaryMedian, CV_MEDIAN, 3, 3, 0, 0);
		blobExtraction(IeyeBinaryMedian, PUPIL_MIN_AREA, pupilCenterAprx, &numPupils);
        //radiigrad(Ieye, pupilCenterAprx, &pupilCenter);
       
        //blob extraction sometimes finds false pupils, they are discarded if the distance to image center is over 50
        for(z=0; z<numPupils; z++)
	    {
            CvPoint2D32f p=cvPoint2D32f(IeyeBinaryMedian->width/2, IeyeBinaryMedian->height/2);
		    int d = EulerianDistance(&pupilCenterAprx[z], &p);
            fprintf(stderr, "\nd %i", d);
		    if(d<50)
		    {
		        radiigrad(Ieye, &pupilCenterAprx[z], &pupilCenter);
                break;
                
		    }
	    }
    
		cvCircle(IeyeRGB, cvPoint((int)pupilCenter.x, (int)pupilCenter.y), 10, cvScalar(0,255,0,0), 1, CV_AA, 0);
		cvShowImage("eye", IeyeRGB);

		if(&pupilCenter==NULL)
		{
			fprintf(stderr, "\nERROR: No pupil...");
            if(eyeWinAbove==False)
                failedFrames++;

			continue;
		}

		succeeded = gazevect(&pupilCenter, glintCenter, numGlints, GazeVect);

		if(succeeded==False)
        {
            if(eyeWinAbove==False)
                failedFrames++;

			continue;            
        }

		if(calibration==True)
		{
            saveCalibrationData(&calib, GazeVect, &screenSize);
			/*if(ignoreCalibPoint==False)
			{
				fprintf(stderr,"\nallocating memory for data...");
				collectedDataX[validSamples]=malloc(4*sizeof(float));
				collectedDataY[validSamples]=malloc(4*sizeof(float));
				refPoints[validSamples]=malloc(2*sizeof(int));
				fprintf(stderr,"\nsaving data...");
				CvPoint2D32f p= ProjectToCartesianCoord(calibPoint.x, calibPoint.y, &screenSize);
				refPoints[validSamples][0]=p.x;
				refPoints[validSamples][1]=p.y;

				for(z=0; z<4; z++)
				{
					collectedDataX[validSamples][z]=GazeVect[z].x;
					collectedDataY[validSamples][z]=GazeVect[z].y;
				}
				validSamples++;
			}
			else
			{
				fprintf(stderr,"\npoint ignored...");
				if(ignoredCalibPoints==ErrorMarginal)
				{
					ignoreCalibPoint=False;
					ignoredCalibPoints=0;

				}
				ignoredCalibPoints++;
				
			}*/
			continue;
		}
		
		match(GazeVect, &model_);
		
		CvPoint c=ProjectToImgCoord(gazeX, gazeY, &screenSize);
		fprintf(stderr,"\nprojected coordinates x:%i  y:%i\n", c.x, c.y);

		//memset(&buffer, 0, sizeof(buffer));
		buffer[0]=0;
		len=composeMessage(c.x, c.y, buffer);

		if (sendto(sock, buffer, len, 0, (struct sockaddr *)&server, sizeof(server))<0)
        { 
            //fprintf (stderr,"\nERROR: unable to send the coordinates to ip: %s port: %i", HOST_ADDR, PORT);   
        }

        if(updateTemplate==True /*&& cost<COST_LIMIT*/)
		{
			cvReleaseImage(&template);
            template = getReferenceTemplate(sImg, (int)round((pupilCenter.x) + (Sx-REF_DX)/scale_factor), (int)round((pupilCenter.y) + (Sy-REF_DY)/scale_factor), False);
			//template = getReferenceTemplate(img, Sx/scale_factor, Sy/scale_factor);
			fprintf(stderr,"\ntemplate updated...");
		}

        if(eyeWinAbove==True)
        {
            succeededFrames++;
        }

	}//while

	close(sock);
    cvReleaseMat(&result_Matrice);
	cvReleaseImage(&sImg);
    cvReleaseImage(&frame_lbpImg);
	cvReleaseImage(&cropImg);
    cvReleaseImage(&cropImg2);
	cvReleaseImage(&Ieye);
	cvReleaseImage(&IeyeRGB);
	cvReleaseImage(&glintsImg);
	cvReleaseImage(&IeyeBinary);
	cvReleaseImage(&IeyeBinaryMedian);
	cvDestroyWindow("eye");
	cvReleaseCapture(&capture);
	//free(modelData);

    //release global images and matrices
    cvReleaseImage(&enlarged_img);
    cvReleaseImage(&block);
    cvReleaseImage(&temp);
    cvReleaseImage(&upsImg);
    cvReleaseImage(&imgMedian);
    cvReleaseMat(&d1);
    cvReleaseMat(&d1Avg);

	return 0;
}

void LBP(IplImage *img, IplImage *lbpImg)
{

	int i, j;
	double center;
	unsigned char lbp_code;
	CvSize size=cvGetSize(img);
	cvSetZero(lbpImg);


	for(i=1; i<size.height-1; i++)
	{
		for(j=1; j<size.width-1; j++)
		{
            lbp_code = 0;
			center = cvGetReal2D(img, i, j);      
            
			lbp_code |= (center <= cvGetReal2D(img, i-1, j-1)) <<0;
            lbp_code |= (center <= cvGetReal2D(img, i, j-1)) <<1;
            lbp_code |= (center <= cvGetReal2D(img, i+1, j-1)) <<2;
            lbp_code |= (center <= cvGetReal2D(img, i-1, j)) <<3;
            lbp_code |= (center <= cvGetReal2D(img, i+1, j)) <<4;
            lbp_code |= (center <= cvGetReal2D(img, i-1, j+1)) <<5;
            lbp_code |= (center <= cvGetReal2D(img, i, j+1)) <<6; 
            lbp_code |= (center <= cvGetReal2D(img, i+1, j+1)) <<7;  
                        
           cvSetReal2D(lbpImg, i, j, lbp_code); 
		}
	}
}

void lbpcomp(IplImage *img, IplImage *img2, CvMat* result)
{

	int block_result=0;
	CvSize size=cvGetSize(img);
	CvSize block_size=cvGetSize(img2);
	CvRect rect;
	int i, j;
	int block_width = block_size.width; 
	int block_height = block_size.height;
	int image_width = img->width; 
	int image_height = img->height;

    enlarged_img=allocateImage(enlarged_img, cvSize(image_width+block_width, image_height+block_height), img->depth, img->nChannels);
    block=allocateImage(block, block_size, enlarged_img->depth, enlarged_img->nChannels);
	//IplImage *enlarged_img = cvCreateImage(cvSize(image_width+block_width, image_height+block_height), img->depth, img->nChannels ); //enlarge the search area
	//IplImage *block = cvCreateImage(block_size, enlarged_img->depth, enlarged_img->nChannels);
        
	CvPoint offset = cvPoint(block_width/2, block_height/2); 
	cvCopyMakeBorder(img, enlarged_img, offset, IPL_BORDER_CONSTANT, cvScalarAll(0));

	//printf("\nblock width= %i    block height= %i\n", block_width, block_height);
	//printf("\ntemp image width= %i    temp image height= %i\n", enlarged_img->width, enlarged_img->height);

	for(i=0; i<enlarged_img->height-block_height; i++)
	{
		for(j=0; j<enlarged_img->width-block_width; j++)
		{
			rect = cvRect(j, i, block_width, block_height); 
       		cvSetImageROI(enlarged_img,rect); 
       		cvCopy(enlarged_img, block, NULL);
       		cvResetImageROI(enlarged_img);
       		block_result = lbpcomp_block(block, img2);
			//printf("\nblock result= %f\n", block_result);
			cvSetReal2D(result, i, j, (double)(block_result));
		}
	}
	//cvReleaseImage(&block);
	//cvReleaseImage(&enlarged_img);
}

int lbpcomp_block(IplImage *img, IplImage *img2)
{

	if((img->width!=img2->width) && (img->height!=img2->height))
	{
		fprintf(stderr, "\nERROR:Input blocks with differing dimensions...");
		exit(1);
	}
	
	unsigned char rawData[2*REF_DX*2*REF_DY];
	unsigned char rawData2[2*REF_DX*2*REF_DY];
	int x, y, len;
	int widthStep=img->widthStep;
	int widthStep2=img2->widthStep;

	for(y = 0; y < img->height; y++)
	{
	    for(x = 0; x < img->width; x++)
		{
	        rawData[y*img->width + x] = (unsigned char)(img->imageData[y*widthStep + x]);
			//printf("\n%i", rawData[y*img->width + x]);
			rawData2[y*img2->width + x] =(unsigned char)(img2->imageData[y*widthStep2 + x]);
			//printf("  %i", rawData2[y*img->width + x]);
		}
	}
	
	len=img->height*img->width;
	return lbpcomp_arrays(rawData, rawData2, len);

}


int lbpcomp_arrays(unsigned char *a, unsigned char *b, int i)
{

	//printf("\nlbpcomp_array\n");
	unsigned int v;				/* count the number of bits set in v     */
	unsigned int c = 0;			/* c accumulates the total bits set in v */
	
	for (; i > 0;) 
	{
		/* Like the Brian Kernighan's way */
		for (v = a[--i] ^ b[i];  v; c++) 
		{
			v &= v - 1;		/* clear the least significant bit set */
		}
	}
	return c;
}

void glintextract(IplImage *img, IplImage *img2, IplImage *resultImg)
{
	//IplImage *temp=0;
	//IplImage *upsImg=0;
	double max, min;
	int new_height = (img2->height)*(1/scale_factor);
	int new_width =(img2->width)*(1/scale_factor);

	if(Th<0)
	{
		//printf("\nimg width= %i    img height= %i\n   nChannels= %i\n", img->width, img->height, img->nChannels);
		cvMinMaxLoc(img, NULL, &max, NULL, NULL, NULL);
		Th = 153;
	}
	
    upsImg=allocateImage(upsImg, cvSize(new_width, new_height), img2->depth, img2->nChannels);
    temp=allocateImage(temp, cvSize(new_width, new_height), img2->depth, img2->nChannels);
	//upsImg = cvCreateImage(cvSize((int)(new_width), (int)(new_height)), img2->depth, img2->nChannels);
	//temp = cvCreateImage(cvSize((int)(new_width), (int)(new_height)), img2->depth, img2->nChannels);									  
	cvResize(img2, upsImg, CV_INTER_CUBIC);	
	cvSub(img, upsImg, temp, NULL);
	cvCmpS(temp, Th, resultImg, CV_CMP_GT);

	//cvReleaseImage(&upsImg);
	//cvReleaseImage(&temp);

}

void blobExtraction(IplImage *img, int min_blobArea, CvPoint2D32f *blobCenters, int* numBlobs)
{

	int i,j, contours_num=0;
	CvMemStorage* memStorage = 0;
	CvSeq *contours=0, *ptr=0;
	CvRect rect;

	if(memStorage==NULL)
	{
		memStorage = cvCreateMemStorage(0);
	}
	else
	{
		cvClearMemStorage(memStorage);
	}

	//blob extraction
	//printf("\nimg width= %i    img height= %i   nChannels= %i\n", img->width, img->height, img->nChannels);
	cvFindContours(img, memStorage, &contours, sizeof(CvContour), CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0));
	
	if(contours==NULL)
	{
		blobCenters=NULL;
		*numBlobs=0;
		return;
	}

	//calculate the center of mass for the blobs
	j=0;
	for(i=0, ptr=contours; ptr != NULL; ptr=ptr->h_next, i++)
	{		               
    	rect = cvBoundingRect(ptr, 0);

		//printf("\nblob area: %i", rect.width*rect.height);
		//printf("   center of mass: x=%i  y=%i", rect.x+rect.width/2, rect.y+rect.height/2);

		if(rect.width*rect.height>=min_blobArea)
		{
			blobCenters[j]=cvPoint2D32f(rect.x+rect.width/2, rect.y+rect.height/2);
			j++;
			//printf("   accepted");
		}
	}
	*numBlobs=j;
	cvReleaseMemStorage(&memStorage);
}   

void radiigrad(IplImage *img, CvPoint2D32f *point, CvPoint2D32f *resultPoint)
{
	int nr = 32, iterMax=12, y=0, x=0,i=0;
	int widthStep=img->widthStep;
	int filterSize=3;
    double D[nr][2];
	double dx=0, dy=0, px=0, py=0, i2=0, i4=0;
	double min=0; 
	double pointX=(double)(point->x); 
	double pointY=(double)(point->y);
	double imgWidth=(double)(img->width); 
	double imgHeight=(double)(img->height);
	double centerX=0;
	double centerY=0;
	CvScalar mean;
	//IplImage *imgMedian=0;
	//CvMat *d1=0, *d1Avg=0; 
    CvMat *temp=0;
	CvPoint max_loc;
	CvPoint2D32f centerPoints[nr];

	for(i=1; i<nr; i++)
	{
		D[i][0]=sin(2*PI*i/nr);
		//printf("\nsin: %f\n", D[i][0]);
		D[i][1]=cos(2*PI*i/nr);
		//printf("cos: %f\n", D[i][1]);
	}	
		
	mean=cvAvg(img, NULL);
	cvMinMaxLoc(img, &min, NULL, NULL, NULL, NULL);
	//printf("\nmean=%f\n", mean.val[0]);
	//printf("\nmin=%f\n", min);

	//Remove corneal reflctions caused by NIR illuminators
	for(y = 0; y < img->height; y++)
	{
	    for(x = 0; x < img->width; x++ )
		{
	        if((double)(img->imageData[y*widthStep + x]) > mean.val[0])
		    img->imageData[y*widthStep + x] = (unsigned char)(min);
		}
	}
        
    imgMedian=allocateImage(imgMedian, cvGetSize(img), 8, 1);
	//imgMedian = cvCreateImage(cvGetSize(img), 8, 1);
	cvSmooth(img, imgMedian, CV_MEDIAN, 5, 5, 0, 0);
    d1=allocateMatrice(d1, nr+5+filterSize, iterMax, CV_16SC1);
	//d1 = cvCreateMat(nr+5+filterSize, iterMax, CV_16SC1);
	cvSetZero(d1);	
	//cvReleaseImage(&imgMedian);

	for(y=0; y<nr; y++)
	{
		dx = D[y][0];
		dy = D[y][1];
		px = pointX + dx*2;
		py = pointY +dy*2;

		for(x=0; x<iterMax; x++)
		{
			if((px<3 || py<3) || (px>imgWidth-2 || py>imgHeight-2))
				break;
	

			i2 = cvGetReal2D(img, (int)(round(py-dy)), (int)(round(px-dx)));
			i4 = cvGetReal2D(img, (int)(round(py+dy)), (int)(round(px+dx)));
			cvSetReal2D(d1, (y+5), x, (i4 - i2));
			px = px+dx;
			py = py+dy;

		}
	}

	//get the rows from the end of d1
	temp = cvCreateMat(d1->rows, filterSize, CV_16SC1);
	cvSetZero(temp);

	cvGetRows(d1, temp, d1->rows-2*filterSize, d1->rows,1);

	//set the rows to the beginning of d1
	for (y = 0; y < temp->rows; y++)
	{
		for(x = 0; x < temp->cols; x++)
		{
			cvSetReal2D(d1, y, x, cvGetReal2D(temp, y, x));
		}
	}

	//get the rows from the beginning of d1
	//cvSetZero(temp);
	cvGetRows(d1, temp, 1, 1+filterSize ,1);

	//set the rows to the end of d1
	for (y = 0; y < temp->rows; y++)
	{
		for(x = 0; x < temp->cols; x++)
		{
			cvSetReal2D(d1, d1->rows-filterSize+y, x, cvGetReal2D(temp, y, x));
		}
	}

	d1Avg=allocateMatrice(d1Avg, d1->rows, d1->cols, CV_16SC1);
	//d1Avg = cvCreateMat(d1->rows, d1->cols, CV_16SC1);
	cvSmooth(d1, d1Avg, CV_BLUR, filterSize, filterSize, 0, 0);

	temp=0;
	temp = cvCreateMat(d1Avg->rows, 1, CV_16SC1);

	for(i=0; i<nr; i++)
	{
		//get max for each row
		cvGetRow(d1Avg, temp, i+5);
		cvMinMaxLoc(temp, NULL, NULL, NULL, &max_loc, NULL);
		//printf("\n%i\n", max_loc.x);
		centerX=pointX + (max_loc.x+1)*D[i][0];
		centerY=pointY + (max_loc.x+1)*D[i][1];
        //set the centesr
		centerPoints[i] = cvPoint2D32f(centerX, centerY);
	}

	CvMat mat = cvMat( 1, nr, CV_32FC2, centerPoints);
	CvBox2D ellipse = cvFitEllipse2(&mat);

	*resultPoint=ellipse.center;
}

int gazevect(CvPoint2D32f *pupil, CvPoint2D32f *glints, int numGlints, CvPoint2D32f *resultGazeVect)
{

	int i=0, j=0;
	float distance=0, meanX=0, meanY=0, temp=0;
	CvPoint2D32f validGlints[4];
	CvPoint2D32f tempPoint;
	float atanged[4];

	for(i=0; i<numGlints; i++)
	{
		distance = EulerianDistance(pupil, &glints[i]);
		if(distance<PUPIL_GLINT_MAX_DIST)
		{
			validGlints[j]=glints[i];
			j++;
		}
	}

	if(j<4)
	{
		fprintf(stderr, "\nERROR: %i glints too far...", (4-j));
		return False;		
	}

	for(i=0; i<4; i++)
	{

		validGlints[i].x -= pupil->x;
		validGlints[i].y -= pupil->y;
	}	

	for(i=0; i<4; i++)
	{
		meanX += validGlints[i].x;
		meanY += validGlints[i].y;
	}
	meanX /= 4;
	meanY /= 4;

	//get four-quadrant inverse tangent of the points
	for(i=0; i<4; i++)
	{
		atanged[i] = atan2f((validGlints[i].y-meanY), (validGlints[i].x-meanX));
	}

	//sorts the glints in correct order using the atanged values
	for(i=0; i<3; i++)
	{
		for(j=0; j<3-i; j++)
		{
			if(atanged[j] > atanged[j+1])
			{
				temp = atanged[j];
				tempPoint = validGlints[j];
				atanged[j] = atanged[j+1];
				validGlints[j] = validGlints[j+1];
				atanged[j+1] = temp;
				validGlints[j+1] = tempPoint;
			}
		}
	}

	for(i=0; i<4; i++)
	{
		resultGazeVect[i] = validGlints[i];
		//printf("\nvalid glints %i: x=%f   y=%f", i, validGlints[i].x, validGlints[i].y);
	}

	return True;		
	
}
void model(CvPoint2D32f *vector, float *result)
{
	int i, j;
	//double gazePoint[2];
	float xp2_yp2[4]={0}, xp2_y[4]={0}, x_yp2[4]={0}, xp2[4]={0}, yp2[4]={0}, xy[4]={0}, x[4]={0}, y[4]={0};
	float tmpX=0, tmpY=0;

	//calculate the components
	for(i=0; i<4; i++)
	{
		x[i] = vector[i].x;
		//printf("\nx%i: %f",i, gazevect[i].x);
		y[i] = vector[i].y;
		//printf("\ny%i: %f",i, gazevect[i].y);
		xy[i] = x[i]*y[i];
		//printf("\nxy%i: %f",i, xy[i]);
		xp2[i] = pow((vector[i].x), 2);
		//printf("\nxp2%i: %f",i, xp2[i]);
		yp2[i] = pow((vector[i].y), 2);
		//printf("\nyp2%i: %f",i, yp2[i]);
		xp2_y[i] = xp2[i]*y[i];
		//printf("\nxp2_y%i: %f",i, xp2_y[i]); 
		x_yp2[i] = x[i]*yp2[i];
		//printf("\nx_yp2%i: %f",i, x_yp2[i]);
		xp2_yp2[i] = xp2[i]*yp2[i];
		//printf("\nxp2_yp2%i: %f",i, xp2_yp2[i]); 
	}

	//organize the components
	for(i=0; i<4; i++)
	{
		result[i] = xp2_yp2[i];
		result[i+4] = x_yp2[i];
		result[i+8] = yp2[i];
		result[i+12] = xp2_y[i];
		result[i+16] = xy[i];
		result[i+20] = y[i];
		result[i+24] = xp2[i];
		result[i+28] = x[i];	
	}
	result[32]=1.0f;
}
void match(CvPoint2D32f *gazevect, struct model *m)
{

	int i, j;
	float gazeParams[33]={0};
	float tmpX=0, tmpY=0;

    /*fprintf(stderr,"\nModel: %i parameters", m->DataSize.height);

	for(i=0; i<m->DataSize.height; i++)
	{
		fprintf(stderr, "\nmodelData %i: x=%f   y=%f", i, m->Data[i][0], m->Data[i][1]);
	}*/

	/*for(i=0; i<4; i++)
	{
		printf("\ngazevect %i: x=%f   y=%f", i, gazevect[i].x, gazevect[i].y);
	}*/

	//calculate the components
	model(gazevect, gazeParams);

	for(i=0; i<33; i++)
	{
		tmpX+=gazeParams[i]*m->Data[i][0];
		tmpY+=gazeParams[i]*m->Data[i][1];
	}


	//sometimes tmpX and tmpY gets really high or low values that messes the gaze coordinates.
	if((abs(tmpX)>1000) || (abs(tmpY)>1000))
	{
		tmpX=0;
		tmpY=0;
	}

	if(gazeX!=0 /*&& gazeY==0*/)
	{
		gazeX = (gazeX + tmpX)/2;
		gazeY = (gazeY + tmpY)/2;
	}
	else
	{
		gazeX=tmpX;
		gazeY=tmpY;
	}
}

void CalculateModelData(float **dataX, float **dataY, int **refPoints, int numSamples, struct model *resultModel)
{
	int i, j, k;
	double d;
	float modelParams[33]={0};
    struct size modelSize; 
	//float **resultModel;
	CvMat *Matrix=0;
	CvMat *InverseMatrix=0;
	CvPoint2D32f vector[4];	

	fprintf(stderr,"\ncalculating model...");
	Matrix=cvCreateMat(numSamples, 33, CV_32FC1);
	InverseMatrix=cvCreateMat(33, numSamples, CV_32FC1);
	
    modelSize.height=33;
    modelSize.width=2;
    resultModel->Data=allocate2DFloatArray(modelSize);
    resultModel->DataSize=modelSize;
    //resultModel->Data = malloc(33*sizeof(float*));

	for (i=0; i<Matrix->rows; i++)
	{
		//construct vector
		for(k=0; k<4; k++)
		{
			vector[k]=cvPoint2D32f(dataX[i][k], dataY[i][k]);
		}
				
		model(vector, modelParams);

		for(j=0; j<Matrix->cols; j++)
		{
			cvSetReal2D(Matrix, i,j, modelParams[j]);
		}
	}

	//gets the inverse matrix
	cvInvert(Matrix, InverseMatrix, CV_SVD);

	//matrix multiplication
	for (i=0; i<InverseMatrix->rows; i++)
	{
		//resultModel->Data[i] =malloc(2*sizeof(float));
		resultModel->Data[i][0]=0.0f;
		resultModel->Data[i][1]=0.0f;
		for(j=0; j<InverseMatrix->cols; j++)
		{
			d=0;
			d=cvGetReal2D(InverseMatrix, i,j);
			resultModel->Data[i][0]+=((float)refPoints[j][0])*d;
			resultModel->Data[i][1]+=((float)refPoints[j][1])*d;
		}
	}
	fprintf(stderr,"\nmodel calculated...");
	writeModelDataFile("ModelData.txt", resultModel->Data, resultModel->DataSize.height);


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	printf("\ntest..................");

	float x=0.0f, y=0.0f;
	double errorX=0, errorY=0;
	fprintf(stderr,"\nmatrix rows: %i cols: %i", Matrix->rows, Matrix->cols);
	for(i=0; i<Matrix->rows; i++)
	{
		x=0.0f; y=0.0f;
		for(j=0; j<Matrix->cols; j++)
		{
			d=0;
			d=cvGetReal2D(Matrix, i,j);
		//	printf("\nd: %f", d);
			x += ((float)resultModel->Data[j][0])*d;
			y += ((float)resultModel->Data[j][1])*d;
		//	printf("\nresultModel[j][0]*d: %f*%f= %f",resultModel[j][0], d,resultModel[j][0]*d);
		}
		errorX += abs((float)refPoints[i][0]-x);
		errorY += abs((float)refPoints[i][1]-y);
		fprintf(stderr,"\nx:%i test x:%f y:%i test y:%f\n", refPoints[i][0], x, refPoints[i][1], y);
	}
	errorX=errorX/Matrix->rows;
	errorY=errorY/Matrix->rows;
	fprintf(stderr,"\nmean error x: %f pixels   mean error y: %f pixels", errorX, errorY);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	cvReleaseMat(&Matrix);
	cvReleaseMat(&InverseMatrix);
	//exit(0);
	//return resultModel;	
}

void readModelDataFile(char *fileName, struct model *m)
{
	char *pch;
	char ch;
	int i=0, j=0, lines=0;
	//size_t len=0;
	char buffer[30];
	//float **modelData=0;
    struct size fileSize;
	FILE *file;
	file=fopen(fileName, "r");

	if(file==NULL)
	{
		fprintf(stderr,"\nERROR: cannot open file");
		exit(0);
	}
	else
	{
		
		//gets the number of lines in a file
		while((ch=fgetc(file))!=EOF)
		{
			if(ch=='\n') 
		 		lines++; 
		}
        fileSize.height=lines;
        fileSize.width=2;
		//m->Data = malloc(lines*sizeof(float*));
        m->Data=allocate2DFloatArray(fileSize);
		rewind(file);

		//while(fgets(buffer, 30, file) != NULL)
		for(i=0; i<lines; i++)
		{
			fgets(buffer, 30, file);
			//m->Data[i] =malloc(2*sizeof(float));
			pch = strtok(buffer," ");
			j=0;

			while(pch != NULL)
			{
				m->Data[i][j]=atof(pch);
				pch = strtok(NULL, " ");
				j++;
			}
		}
	}
	fclose(file);

	m->DataSize.height=lines;
	//return modelData;
}

void writeModelDataFile(char *fileName, float **inputData, int lines)
{
	//size_t len=0;
	int i=0;
	FILE *file;
	file=fopen(fileName, "w");

	fprintf(stderr,"\nwriting file\n");

	if(file==NULL)
	{
		fprintf(stderr,"\nERROR: cannot open file\n");
		exit(0);
	}
	else
	{
		//fwrite(inputData, sizeof(char), len, file);
		while(i<lines)
		{
			if(inputData[i]!=NULL)
				fprintf(file, "%.9g %.9g\n", inputData[i][0], inputData[i][1]);

			i++;
		}
	}
	fclose(file);
}

float** allocate2DFloatArray(struct size s)
{
    int j;
    float **array=0;
    array=malloc(s.height*sizeof(float*));

    if(array==NULL)
	{
	    fprintf(stderr, "\nERROR: Couldn't allocate model parameters...");
        exit(-1);
	}
    
    for(j=0; j<s.height; j++)
    {
        array[j]=malloc(s.width*sizeof(float));

        if(array[j]==NULL)
	    {
	        fprintf(stderr, "\nERROR: Couldn't allocate model parameters...");
            exit(-1);
	    }
    }

    return array;

}

void free2DFloatArray(struct size s, float **array)
{

    int j;

    for(j=0; j<s.height; j++)
	{
	    free(array[j]);
	}
	
    free(array);    

}

int** allocate2DIntArray(struct size s)
{
    int j;
    int **array=0;
    array=malloc(s.height*sizeof(int*));

    if(array==NULL)
	{
	    fprintf(stderr, "\nERROR: Couldn't allocate model parameters...");
        exit(-1);
	}
    
    for(j=0; j<s.height; j++)
    {
        array[j]=malloc(s.width*sizeof(int));

        if(array[j]==NULL)
	    {
	        fprintf(stderr, "\nERROR: Couldn't allocate model parameters...");
            exit(-1);
	    }
    }

    return array;

}

void free2DIntArray(struct size s, int **array)
{

    int j;

    for(j=0; j<s.height; j++)
	{
	    free(array[j]);
	}
	
    free(array);    

}

void initCalibration(struct calibration *calib, struct size *screenSize)
{

    //IplImage *calibImg=0;
	calib->vertical_mov=screenSize->width/(CALPOINTS_X*CALPOINTS_X-1);
	calib->horizontal_mov=screenSize->height/(CALPOINTS_Y*CALPOINTS_Y-1);
	calib->calibPointPos=1;
	calib->validSamples=0;
    calib->ignoredCalibPoints=0;
	//calib->samplesNum=CALPOINTS_X*CALPOINTS_Y*CALPOINT_FRAMES;
	//calibration strating point
	calib->calibPoint=cvPoint(calib->vertical_mov, calib->horizontal_mov);

    calib->SizeY.height=CALPOINTS_X*CALPOINTS_Y*CALPOINT_FRAMES;
    calib->SizeX.height=CALPOINTS_X*CALPOINTS_Y*CALPOINT_FRAMES;
    calib->SizeRefpoints.height=CALPOINTS_X*CALPOINTS_Y*CALPOINT_FRAMES;

    calib->SizeY.width=4;
    calib->SizeX.width=4;
    calib->SizeRefpoints.width=2;

    calib->collectedDataX=allocate2DFloatArray(calib->SizeX);
	calib->collectedDataY=allocate2DFloatArray(calib->SizeY);
	calib->refPoints=allocate2DIntArray(calib->SizeRefpoints);

	cvNamedWindow("calibration", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("calibration", 0, 0);
	calib->calibImg = cvCreateImage(cvSize(screenSize->width, screenSize->height),8,3);
	cvCircle(calib->calibImg, calib->calibPoint , 15, cvScalar(255,255,255,0), -1, CV_AA, 0);

}

void updateCalibration(int frameNum, struct calibration *calib, struct model *m)
{

    if(frameNum%CALPOINT_FRAMES==0 && frameNum!=0)
	{
	    cvSetZero(calib->calibImg);
		if(calib->calibPointPos%CALPOINTS_X==0)
		{
		    calib->calibPoint.x=calib->vertical_mov;
			calib->calibPoint.y+=calib->horizontal_mov*CALPOINTS_Y;
		}
		else
		    calib->calibPoint.x+=calib->vertical_mov*CALPOINTS_X;
					
		calib->calibPointPos++;
		ignoreCalibPoint=True;
		cvCircle(calib->calibImg, calib->calibPoint , 15, cvScalar(255,255,255,0), -1, CV_AA, 0);
	}
			
	cvShowImage("calibration", calib->calibImg);
		
	if(calib->calibPointPos==CALPOINTS_X*CALPOINTS_Y+1)
	{
	    calibration=False;
		cvReleaseImage(&calib->calibImg);
		cvDestroyWindow("calibration");

		//for(z=0; z<modelDataLen; z++)
		//{
		//	free(modelData[z]);
		//}
		//free(modelData);
        free2DFloatArray(m->DataSize, m->Data);

		//modelData=CalculateModelData(collectedDataX, collectedDataY, refPoints, validSamples);
        CalculateModelData(calib->collectedDataX, calib->collectedDataY, calib->refPoints, calib->validSamples, m);
		//free the calibration data not needed anymore
		//for(z=0; z<validSamples; z++)
		//{
		//	free(collectedDataX[z]);
		//	free(collectedDataY[z]);
		//}
		//free(collectedDataX);
		//free(collectedDataY);
        free2DFloatArray(calib->SizeX, calib->collectedDataX);
        free2DFloatArray(calib->SizeY, calib->collectedDataY);
	}

}

void saveCalibrationData(struct calibration *calib, CvPoint2D32f *GazeVect, struct size *screenSize)
{
    int z=0;

    if(ignoreCalibPoint==False)
	{
		//fprintf(stderr,"\nallocating memory for data...");
		//collectedDataX[validSamples]=malloc(4*sizeof(float));
		//collectedDataY[validSamples]=malloc(4*sizeof(float));
		//refPoints[validSamples]=malloc(2*sizeof(int));
		fprintf(stderr,"\nsaving data...");
		CvPoint2D32f p= ProjectToCartesianCoord(calib->calibPoint.x, calib->calibPoint.y, screenSize);
		calib->refPoints[calib->validSamples][0]=p.x;
		calib->refPoints[calib->validSamples][1]=p.y;

		for(z=0; z<4; z++)
		{
		    calib->collectedDataX[calib->validSamples][z]=GazeVect[z].x;
			calib->collectedDataY[calib->validSamples][z]=GazeVect[z].y;
		}
		calib->validSamples++;
	}
	else
	{
	    fprintf(stderr,"\npoint ignored...");
		if(calib->ignoredCalibPoints==ErrorMarginal)
		{
		    ignoreCalibPoint=False;
			calib->ignoredCalibPoints=0;

		}
		calib->ignoredCalibPoints++;
				
	}
}

IplImage* getReferenceFrame()
{

	CvCapture *capture = 0;
	capture = cvCaptureFromCAM(VID_DEV);
	IplImage * frameRGB=0;
	IplImage * frameRGB_mirror=0;

   	if ( !capture ) 
	{
     		fprintf(stderr, "\nERROR: capture is NULL...");
     		exit(1);
   	}

   	cvNamedWindow("refwindow", CV_WINDOW_AUTOSIZE);

   	while(1) 
	{
        IplImage* frame = cvQueryFrame(capture);
     	if (!frame) 
		{
       	    fprintf( stderr, "\nERROR: frame is null..." );
       		break;
     	}

     	frameRGB = cvCreateImage(cvGetSize(frame), frame->depth,3);
		frameRGB_mirror = cvCreateImage(cvGetSize(frame), frame->depth,3);
		cvCvtColor(frame, frameRGB, CV_GRAY2BGR);

		if ( (cvWaitKey(10) & 255) == 27 )
		{
			cvSaveImage("refImage.png", frameRGB, 0);
			break;
		}

		cvLine(frameRGB, cvPoint(REF_IMG_X-10, REF_IMG_Y), cvPoint(REF_IMG_X+10, REF_IMG_Y), cvScalar(0,0,255,0), 1, CV_AA, 0);
		cvLine(frameRGB, cvPoint(REF_IMG_X, REF_IMG_Y-10), cvPoint(REF_IMG_X, REF_IMG_Y+10), cvScalar(0,0,255,0), 1, CV_AA, 0);
		cvFlip(frameRGB, frameRGB_mirror, 1);
		cvShowImage("refwindow", frameRGB_mirror);
     	cvReleaseImage(&frameRGB);
		cvReleaseImage(&frameRGB_mirror);
   	}

   	cvReleaseCapture(&capture);
   	cvDestroyWindow("refwindow");
   	return frameRGB; // exit(0);
}

IplImage* getReferenceTemplate(IplImage* refImg, int x, int y, int downscaleImg)
{

	//IplImage *ref_sImg=0;
	//IplImage *ref_lbpImg=0;
	//IplImage *cropImg=0;
	IplImage *template=0;
	int new_height = (int)((refImg->height)*scale_factor);
	int new_width =(int)((refImg->width)*scale_factor);

    //0.05 and 0.95 scaled up because IplImages' depths are 8.
	//int weight1=50, weight2=950;
    float weight1=0.05, weight2=0.95;
	int i,j,w,h;
    double d1=0, d2=0, tempRes=0;
    CvRect rect;

    if(downscaleImg==True)
    {

	    if(refImg->nChannels!=1)
	    {
		    IplImage *grImg = cvCreateImage(cvGetSize(refImg), 8, 1);
		    cvCvtColor(refImg, grImg, CV_BGR2GRAY);
            ref_sImg=allocateImage(ref_sImg, cvSize(new_width, new_height),grImg->depth,grImg->nChannels);
		    //ref_sImg = cvCreateImage(cvSize(new_width, new_height),grImg->depth,grImg->nChannels);									 
            downscale(grImg, ref_sImg);		
            //cvResize(grImg, ref_sImg, CV_INTER_LINEAR);
		    cvReleaseImage(&grImg);
	    }
	    else
	    {
            ref_sImg=allocateImage(ref_sImg, cvSize(new_width, new_height),8,1);
		    //ref_sImg =  cvCreateImage(cvSize(new_width, new_height),8,1);
            downscale(refImg, ref_sImg);									 
		    //cvResize(refImg, ref_sImg, CV_INTER_LINEAR);
	    }
    }
    else
    {
        ref_sImg=allocateImage(ref_sImg, cvGetSize(refImg), 8, 1);
        //ref_sImg = cvCreateImage(cvGetSize(refImg), 8, 1);
        cvCopy(refImg, ref_sImg, NULL);    
    }    
    
	//get the scaled down reference image's centerpoint
	CvPoint image_center = cvPoint(round((double)x*scale_factor), round((double)y*scale_factor));
	
	image_center.x = min(max(image_center.x, REF_DX+1), ref_sImg->width-REF_DX);
    image_center.y = min(max(image_center.y, REF_DY+1), ref_sImg->height-REF_DY);

    ref_lbpImg=allocateImage(ref_lbpImg, cvGetSize(ref_sImg),8, 1);
	//ref_lbpImg = cvCreateImage(cvGetSize(ref_sImg),8, 1);
	LBP(ref_sImg, ref_lbpImg);
    //cvSaveImage("ref_lbpImg.png", ref_lbpImg, 0);
	cvSetImageROI(ref_lbpImg, cvRect(image_center.x-REF_DX, image_center.y-REF_DY, 2*REF_DX-1, 2*REF_DY-1));
	template = cvCreateImage(cvGetSize(ref_lbpImg), ref_lbpImg->depth, ref_lbpImg->nChannels);
    cvResetImageROI(ref_lbpImg);


    //cvCopy(ref_lbpImg, template, NULL);
	//cvResetImageROI(ref_lbpImg);

    //updates the template by calculating weighted average of the current and new template
    if(ref_lbpImgCurrent!=NULL)
    {
    
        for(h=0, i=image_center.y-REF_DY; i<image_center.y-REF_DY + (2*REF_DY-1); i++, h++)
		{
			for(w=0, j=image_center.x-REF_DX; j<image_center.x-REF_DX + (2*REF_DX-1); j++, w++)
			{  
                d1=cvGetReal2D(ref_lbpImg, i, j);
                d2=cvGetReal2D(ref_lbpImgCurrent, h, w);
				tempRes=round((d1*weight1 + d2*weight2));//(d1*weight1 + d2*weight2)/1000;
				cvSetReal2D(template, h, w, tempRes);
                //fprintf(stderr, "\n d1:%f  d2:%f  tempRes:%f", d1,d2,tempRes);
                //fprintf(stderr, "\n i:%d  j:%d w:%i h:%d", i,j,h,w); 
			}
		}

        cvSetImageROI(ref_lbpImg, cvRect(image_center.x-REF_DX, image_center.y-REF_DY, 2*REF_DX-1, 2*REF_DY-1));
        ref_lbpImgCurrent=allocateImage(ref_lbpImgCurrent, cvGetSize(ref_lbpImg),8, 1);
        cvCopy(ref_lbpImg, ref_lbpImgCurrent, NULL);
        cvResetImageROI(ref_lbpImg);
        //cvSaveImage("ref_lbpImg.png", ref_lbpImg, 0);
        //cvSaveImage("ref_lbpImgCurrent.png", ref_lbpImgCurrent, 0);
        //cvSaveImage("template.png", template, 0);
        //exit(0);
    }
    else
    {
        cvSetImageROI(ref_lbpImg, cvRect(image_center.x-REF_DX, image_center.y-REF_DY, 2*REF_DX-1, 2*REF_DY-1));
        cvCopy(ref_lbpImg, template, NULL);

        ref_lbpImgCurrent=allocateImage(ref_lbpImgCurrent, cvGetSize(ref_lbpImg),8, 1);
        cvCopy(ref_lbpImg, ref_lbpImgCurrent, NULL);
        cvResetImageROI(ref_lbpImg);
	}


	////////////////cropping before LBP/////////////////////////////////////////////////////
	/*cvSetImageROI(ref_sImg, cvRect(image_center.x-REF_DX-1, image_center.y-REF_DY-1, 2*REF_DX+1, 2*REF_DY+1));
	cropImg = cvCreateImage(cvGetSize(ref_sImg),ref_sImg->depth, ref_sImg->nChannels);
	cvCopy(ref_sImg, cropImg, NULL);
	cvResetImageROI(ref_sImg);

	ref_lbpImg = cvCreateImage(cvGetSize(cropImg),8, 1);
	
	LBP(cropImg, ref_lbpImg);
	cvReleaseImage(&cropImg);
	//cvSaveImage("ref_lbpImg.png", ref_lbpImg, 0);

	//cut the corners where the lbp values are distorted
	new_height = ref_lbpImg->height-2;
	new_width = ref_lbpImg->width-2;	
	cvSetImageROI(ref_lbpImg, cvRect(1, 1, new_width, new_height));
	template = cvCreateImage(cvGetSize(ref_lbpImg),ref_lbpImg->depth, ref_lbpImg->nChannels);
	cvCopy(ref_lbpImg, template, NULL);
	cvResetImageROI(ref_lbpImg);*/


	//cvReleaseImage(&ref_sImg);
	//cvReleaseImage(&ref_lbpImg);
	return template;

}

        
int filter(int data[])
{
    int result;

    //coefficients [-1 2 3 4 4 3 2 -1]
	result  =  data[2] + data[5];
	result +=              result << 1;
	result += (data[3] + data[4]) << 2;
	result += (data[1] + data[6]) << 1;
	result -=  data[0] + data[7];
        
    //result = (result + 8) >> 4;
    return result;

}

void downscale(IplImage *srcImg, IplImage *destImg)
{
    /*int params[8] ={0};
    int i, j, k, x, y, scaleStep=4, h=srcImg->height+scaleStep, w=srcImg->width+scaleStep, offset=w;
    int imgDataTmp[1028*772]; //imgDataTmp[w*h];
       
    //reads the image data into the buffer
    for(i=0, y=0;  i<h; i++)
	{

        if(i>2 && i<srcImg->height)
            y++;

	    for(j=0, x=0; j<w; j++)
	    {
            if(j>2 && j<srcImg->width)
                x++;

                imgDataTmp[i*w+j] = (unsigned char)(srcImg->imageData[y*srcImg->widthStep+x]);      
        }
    }

    for(k=0; k<2; k++)
    {

        //horizontal scaling
        w=w/scaleStep;
        //printf("\nw: %i", w);
        for(i=0;  i<h; i++)
	    {
	        for(j=0; j<w; j++)
	        {
                params[0] = imgDataTmp[i*offset+j*scaleStep+0];
			    params[1] = imgDataTmp[i*offset+j*scaleStep+1];
			    params[2] = imgDataTmp[i*offset+j*scaleStep+2];
			    params[3] = imgDataTmp[i*offset+j*scaleStep+3];
			    params[4] = imgDataTmp[i*offset+j*scaleStep+4];
			    params[5] = imgDataTmp[i*offset+j*scaleStep+5];
			    params[6] = imgDataTmp[i*offset+j*scaleStep+6];
			    params[7] = imgDataTmp[i*offset+j*scaleStep+7];
                
                imgDataTmp[i*w+j]=filter(params);
		    }
	    }
        offset=offset/scaleStep;

        //vertical scaling
        h=h/scaleStep;
        //printf("\nh: %i", h);
        for(i=0;  i<h; i++)
	    {                       
	        for(j=0; j<w; j++)
	        {
                params[0] = imgDataTmp[(i*scaleStep+0)*w+j];
			    params[1] = imgDataTmp[(i*scaleStep+1)*w+j];
			    params[2] = imgDataTmp[(i*scaleStep+2)*w+j];
			    params[3] = imgDataTmp[(i*scaleStep+3)*w+j];
			    params[4] = imgDataTmp[(i*scaleStep+4)*w+j];
			    params[5] = imgDataTmp[(i*scaleStep+5)*w+j];
			    params[6] = imgDataTmp[(i*scaleStep+6)*w+j];
			    params[7] = imgDataTmp[(i*scaleStep+7)*w+j];
                
                imgDataTmp[i*w+j]=filter(params);
		    }
                        
	   }
    }
                       

    //reads the buffer into the image
    for(i=0;  i<h; i++)
	{
        //fprintf(stderr, "\n");
	    for(j=0; j<w; j++)
	    {
            //destImg->imageData[i*destImg->widthStep+j] = (imgDataTmp[i*w+j] + 16384) >>16;
            cvSetReal2D(destImg, i, j, (imgDataTmp[i*w+j] + 16384) >>16);
            //cvSetReal2D(destImg, i, j, imgDataTmp[i*w+j]);  
        }
    }*/
    //cvSaveImage("downscaled.png", destImg, 0);
    // exit(0);


    int i, j,x=0,y=0, scaleW=16, scaleH=16;
    CvScalar pixelMean;
    CvSize size=cvGetSize(srcImg);
	CvSize sizeDest=cvGetSize(destImg);
	cvSetZero(destImg);

    for(i=0, y=0; i<size.height, y<sizeDest.height; i+=scaleH, y++)
	{
	    for(j=0, x=0; j<size.width, x<sizeDest.width; j+=scaleW, x++)
		{
	        cvSetImageROI(srcImg, cvRect(j, i, scaleW, scaleH));
            pixelMean=cvAvg(srcImg, NULL);
			cvResetImageROI(srcImg);
            cvSetReal2D(destImg, y, x, round(pixelMean.val[0]));	
		}
	}
    //cvSaveImage("downscaled.png", destImg, 0);
    //exit(0);

}

void getScreenSize(struct size *s)
{
	//int width, height; 
	int screen;
	Display *display;
 		
	if ((display = XOpenDisplay(NULL)) == NULL ) 
   	{  
		fprintf(stderr, "\nERROR: cannot get the screen size...");
      	return;
   	}

	screen = DefaultScreen(display);
   	s->width = DisplayWidth(display, screen);
   	s->height = DisplayHeight(display, screen);
	//printf("width: %i height: %i", width, height);

	XCloseDisplay(display);
}

void parseCommandline(int argc, char* argv[], struct model *m, IplImage** refImg/*, bool calib*/)
{
    fprintf(stderr, "\nParsing commandline...");
    int i;

    if(argc<2)
    {

        *refImg = cvLoadImage("refImage.png", CV_LOAD_IMAGE_UNCHANGED);
        readModelDataFile("ModelData.txt", m);
        
        if(refImg==NULL)
        {
            fprintf(stderr, "\nERROR: No reference image available...");
            //usage();
            exit(1);
        }

        if(m->Data==NULL)
        {
            fprintf(stderr, "\nERROR: No model data available...");
            //usage();
            exit(1);
        }
    
    return;        
    }

    i = 1;
    while (i<argc) 
    {
        fprintf(stderr, "\nWhile i:%i", i);
        if (argv[i][0] != '-')
        {
            fprintf(stderr, "\nERROR: Wrong parameter...");
            //usage();
            exit(1);
        }
        if(argv[i][1]=='c') 
        {
            i++;
            *refImg = getReferenceFrame();
            calibration=True;
            break;
        }
        if(argv[i][1]=='i') 
        {
            *refImg = cvLoadImage(argv[i+1], CV_LOAD_IMAGE_UNCHANGED);
            i+=2;
            continue;
        }
        if(argv[i][1]=='m') 
        {
            readModelDataFile(argv[i+1], m);
            i+=2;
            continue;
        }
            
    }

     if(*refImg==NULL)
     {
         *refImg = cvLoadImage("refImage.png", CV_LOAD_IMAGE_UNCHANGED);

         if(refImg==NULL)
         {
             fprintf(stderr, "\nERROR: No reference image available...");
             // usage();
             exit(1);
         }
     }

     if(m->Data==NULL)
     {
         readModelDataFile("ModelData.txt", m);

         if(m->Data==NULL)
         {
             fprintf(stderr, "\nERROR: No model data available...");
             //usage();
             exit(1);
         }
     }

}

int composeMessage(int x, int y, char *message)
{
	char *action="\"GazeCoordinates\"";
	char *scene="\"null\"";
	char *entityName="\"FreeLookCamera\"";
	int len;	

	len = sprintf(message, "{\"op\": \"action\", \"exectype\": \"local\", \"scene\": %s, \"entity\": %s, \"action\": %s, \"params\": [%i, %i]}\r\n",scene, entityName, action, x, y);
	
	return len;
}

void setWindowAvove(char *winName)
{

    GtkWidget* window;
    window = GTK_WIDGET(cvGetWindowHandle(winName));
    gtk_window_set_keep_above(GTK_WINDOW(window), TRUE);
}

void setWindowBelow(char *winName)
{
    GtkWidget* window;
    window = GTK_WIDGET(cvGetWindowHandle(winName));
    gtk_window_set_keep_below(GTK_WINDOW(window), TRUE);
}

IplImage* getImagesfromDir(int frame)
{

    IplImage *img;
    IplImage *grImg=0;
    char fName[27]="";
    char *dirName="capture_20120127/";
    char end[10] = ".png";
    sprintf(fName, "%s%06d%s",dirName, frame, end);
    //puts(fName);
    img=cvLoadImage(fName, CV_LOAD_IMAGE_UNCHANGED);

    if(img==NULL)
        return NULL;
        
    if(img->nChannels!=1)
    {
        grImg = cvCreateImage(cvGetSize(img), 8,1);
	    cvCvtColor(img, grImg, CV_RGB2GRAY);
        return grImg;
    }

    return img; 

}
