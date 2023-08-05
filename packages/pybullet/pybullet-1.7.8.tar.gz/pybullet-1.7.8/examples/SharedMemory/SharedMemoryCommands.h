#ifndef SHARED_MEMORY_COMMANDS_H
#define SHARED_MEMORY_COMMANDS_H

//this is a very experimental draft of commands. We will iterate on this API (commands, arguments etc)

#include "SharedMemoryPublic.h"

#ifdef __GNUC__
	#include <stdint.h>
	typedef int32_t smInt32_t;
	typedef int64_t smInt64_t;
	typedef uint32_t smUint32_t;
	typedef uint64_t smUint64_t;
#elif defined(_MSC_VER)
	typedef __int32 smInt32_t;
	typedef __int64 smInt64_t;
	typedef unsigned __int32 smUint32_t;
	typedef unsigned __int64 smUint64_t;
#else
	typedef int smInt32_t;
	typedef long long int smInt64_t;
	typedef unsigned int smUint32_t;
	typedef unsigned long long int smUint64_t;
#endif

#define SHARED_MEMORY_MAX_STREAM_CHUNK_SIZE (512*1024)

#define SHARED_MEMORY_SERVER_TEST_C
#define MAX_DEGREE_OF_FREEDOM 128
#define MAX_NUM_SENSORS 256
#define MAX_URDF_FILENAME_LENGTH 1024
#define MAX_SDF_FILENAME_LENGTH 1024
#define MAX_FILENAME_LENGTH MAX_URDF_FILENAME_LENGTH
#define MAX_NUM_LINKS MAX_DEGREE_OF_FREEDOM

struct TmpFloat3 
{
    float m_x;
    float m_y;
    float m_z;
};

#ifdef _WIN32
__inline
#else
inline
#endif
TmpFloat3 CreateTmpFloat3(float x, float y, float z) 
{
    TmpFloat3 tmp;
    tmp.m_x = x;
    tmp.m_y = y;
    tmp.m_z = z;
    return tmp;
}

enum EnumSdfArgsUpdateFlags
{
	SDF_ARGS_FILE_NAME=1,
};

struct SdfArgs
{
	char m_sdfFileName[MAX_URDF_FILENAME_LENGTH];
    int m_useMultiBody;
	double m_globalScaling;
};

struct FileArgs
{
	char m_fileName[MAX_URDF_FILENAME_LENGTH];
	int m_stateId;
};

enum EnumLoadStateArgsUpdateFlags
{
	CMD_LOAD_STATE_HAS_STATEID=1,
	CMD_LOAD_STATE_HAS_FILENAME=2,
};

enum EnumUrdfArgsUpdateFlags
{
	URDF_ARGS_FILE_NAME=1,
	URDF_ARGS_INITIAL_POSITION=2,
	URDF_ARGS_INITIAL_ORIENTATION=4,
	URDF_ARGS_USE_MULTIBODY=8,
	URDF_ARGS_USE_FIXED_BASE=16,
	URDF_ARGS_HAS_CUSTOM_URDF_FLAGS = 32,
	URDF_ARGS_USE_GLOBAL_SCALING =64,
};


struct UrdfArgs
{
	char m_urdfFileName[MAX_URDF_FILENAME_LENGTH];
	double m_initialPosition[3];
	double m_initialOrientation[4];
	int m_useMultiBody;
	int m_useFixedBase;
	int m_urdfFlags;
	double m_globalScaling;
};



struct MjcfArgs
{
	char m_mjcfFileName[MAX_URDF_FILENAME_LENGTH];
	int m_useMultiBody;
	int m_flags;
};

struct b3SearchPathfArgs
{
	char m_path[MAX_FILENAME_LENGTH];
};

enum CustomCommandEnum
{
	CMD_CUSTOM_COMMAND_LOAD_PLUGIN=1,
	CMD_CUSTOM_COMMAND_UNLOAD_PLUGIN=2,
	CMD_CUSTOM_COMMAND_EXECUTE_PLUGIN_COMMAND=4,
	CMD_CUSTOM_COMMAND_LOAD_PLUGIN_POSTFIX=8,
};

struct b3CustomCommand
{
	int m_pluginUniqueId;
	b3PluginArguments m_arguments;
	char m_pluginPath[MAX_FILENAME_LENGTH];
	char m_postFix[MAX_FILENAME_LENGTH];

};

struct b3CustomCommandResultArgs
{
	int m_pluginUniqueId;
	int m_executeCommandResult;

};

struct BulletDataStreamArgs
{
	char m_bulletFileName[MAX_FILENAME_LENGTH];
	int m_bodyUniqueId;
	char m_bodyName[MAX_FILENAME_LENGTH];
};

enum EnumChangeDynamicsInfoFlags
{
	CHANGE_DYNAMICS_INFO_SET_MASS=1,
	CHANGE_DYNAMICS_INFO_SET_COM=2,
	CHANGE_DYNAMICS_INFO_SET_LATERAL_FRICTION=4,
	CHANGE_DYNAMICS_INFO_SET_SPINNING_FRICTION=8,
	CHANGE_DYNAMICS_INFO_SET_ROLLING_FRICTION=16,
	CHANGE_DYNAMICS_INFO_SET_RESTITUTION=32,
	CHANGE_DYNAMICS_INFO_SET_LINEAR_DAMPING=64,
	CHANGE_DYNAMICS_INFO_SET_ANGULAR_DAMPING=128,
	CHANGE_DYNAMICS_INFO_SET_CONTACT_STIFFNESS_AND_DAMPING=256,
	CHANGE_DYNAMICS_INFO_SET_FRICTION_ANCHOR = 512,
	CHANGE_DYNAMICS_INFO_SET_LOCAL_INERTIA_DIAGONAL = 1024,

};

struct ChangeDynamicsInfoArgs
{
	int m_bodyUniqueId;
	int m_linkIndex;
	double m_mass;
	double m_COM[3];
	double m_lateralFriction;
	double m_spinningFriction;
	double m_rollingFriction;
	double m_restitution;
	double m_linearDamping;
	double m_angularDamping;
	double m_contactStiffness;
	double m_contactDamping;
	double m_localInertiaDiagonal[3];
	int m_frictionAnchor;
};

struct GetDynamicsInfoArgs
{
	int m_bodyUniqueId;
	int m_linkIndex;
};

struct SetJointFeedbackArgs
{
	int m_bodyUniqueId;
	int m_linkId;
	int m_isEnabled;
};

enum EnumInitPoseFlags
{
    INIT_POSE_HAS_INITIAL_POSITION=1,
    INIT_POSE_HAS_INITIAL_ORIENTATION=2,
    INIT_POSE_HAS_JOINT_STATE=4,
	INIT_POSE_HAS_BASE_LINEAR_VELOCITY = 8,
	INIT_POSE_HAS_BASE_ANGULAR_VELOCITY = 16,
	INIT_POSE_HAS_JOINT_VELOCITY=32,
};


///InitPoseArgs is mainly to initialize (teleport) the robot in a particular position
///No motors or controls are needed to initialize the pose. It is similar to
///moving a robot to a starting place, while it is switched off. It is only called
///at the start of a robot control session. All velocities and control forces are cleared to zero.
struct InitPoseArgs
{
	int m_bodyUniqueId;
	int m_hasInitialStateQ[MAX_DEGREE_OF_FREEDOM];
	double m_initialStateQ[MAX_DEGREE_OF_FREEDOM];
	int m_hasInitialStateQdot[MAX_DEGREE_OF_FREEDOM];
	double m_initialStateQdot[MAX_DEGREE_OF_FREEDOM];
};


struct RequestDebugLinesArgs
{
	int m_debugMode;
    int m_startingLineIndex;
};

struct RequestPixelDataArgs
{
	float m_viewMatrix[16];
	float m_projectionMatrix[16];
	int m_startPixelIndex;
	int m_pixelWidth;
	int m_pixelHeight;
	float m_lightDirection[3];
    float m_lightColor[3];
    float m_lightDistance;
    float m_lightAmbientCoeff;
    float m_lightDiffuseCoeff;
    float m_lightSpecularCoeff;
    int m_hasShadow;
	int m_flags;
};

enum EnumRequestPixelDataUpdateFlags
{
	REQUEST_PIXEL_ARGS_HAS_CAMERA_MATRICES=1,
	REQUEST_PIXEL_ARGS_SET_PIXEL_WIDTH_HEIGHT=2,
	REQUEST_PIXEL_ARGS_SET_LIGHT_DIRECTION=4,
    REQUEST_PIXEL_ARGS_SET_LIGHT_COLOR=8,
    REQUEST_PIXEL_ARGS_SET_LIGHT_DISTANCE=16,
    REQUEST_PIXEL_ARGS_SET_SHADOW=32,
    REQUEST_PIXEL_ARGS_SET_AMBIENT_COEFF=64,
    REQUEST_PIXEL_ARGS_SET_DIFFUSE_COEFF=128,
    REQUEST_PIXEL_ARGS_SET_SPECULAR_COEFF=256,
	REQUEST_PIXEL_ARGS_HAS_FLAGS = 512,

	//don't exceed (1<<15), because this enum is shared with EnumRenderer in SharedMemoryPublic.h
	
};

enum EnumRequestContactDataUpdateFlags
{
	CMD_REQUEST_CONTACT_POINT_HAS_QUERY_MODE=1,
	CMD_REQUEST_CONTACT_POINT_HAS_CLOSEST_DISTANCE_THRESHOLD=2,
	CMD_REQUEST_CONTACT_POINT_HAS_LINK_INDEX_A_FILTER = 4,
	CMD_REQUEST_CONTACT_POINT_HAS_LINK_INDEX_B_FILTER = 8,
};

struct RequestRaycastIntersections
{
	int m_numRays;
	double m_rayFromPositions[MAX_RAY_INTERSECTION_BATCH_SIZE][3];
	double m_rayToPositions[MAX_RAY_INTERSECTION_BATCH_SIZE][3];
};

struct SendRaycastHits
{
	int m_numRaycastHits;
	b3RayHitInfo m_rayHits[MAX_RAY_INTERSECTION_BATCH_SIZE];
};

struct RequestContactDataArgs
{
    int m_startingContactPointIndex;
    int m_objectAIndexFilter;
	int m_objectBIndexFilter;
	int m_linkIndexAIndexFilter;
	int m_linkIndexBIndexFilter;
	double m_closestDistanceThreshold;
	int m_mode;
};

struct RequestOverlappingObjectsArgs
{
	int m_startingOverlappingObjectIndex;
	double m_aabbQueryMin[3];
	double m_aabbQueryMax[3];
};

struct RequestVisualShapeDataArgs
{
	int m_bodyUniqueId;
	int m_startingVisualShapeIndex;
};

struct RequestCollisionShapeDataArgs
{
	int m_bodyUniqueId;
	int m_linkIndex;
};

enum EnumUpdateVisualShapeData
{
	CMD_UPDATE_VISUAL_SHAPE_TEXTURE=1,
	CMD_UPDATE_VISUAL_SHAPE_RGBA_COLOR=2,
	CMD_UPDATE_VISUAL_SHAPE_SPECULAR_COLOR=4,
};

struct UpdateVisualShapeDataArgs
{
    int m_bodyUniqueId;
    int m_jointIndex;
    int m_shapeIndex;
    int m_textureUniqueId;
	double m_rgbaColor[4];
	double m_specularColor[3];
};

struct LoadTextureArgs
{
    char m_textureFileName[MAX_FILENAME_LENGTH];
};

struct b3LoadTextureResultArgs
{
	int m_textureUniqueId;
};

struct SendVisualShapeDataArgs
{
	int m_bodyUniqueId;
    int m_startingVisualShapeIndex;
    int m_numVisualShapesCopied;
    int m_numRemainingVisualShapes;
};

struct SendCollisionShapeDataArgs
{
	int m_bodyUniqueId;
	int m_linkIndex;
	int m_numCollisionShapes;
};

struct SendDebugLinesArgs
{
    int m_startingLineIndex;
	int m_numDebugLines;
    int m_numRemainingDebugLines;
};

struct SendPixelDataArgs
{
	int m_imageWidth;
	int m_imageHeight;

    int m_startingPixelIndex;
    int m_numPixelsCopied;
    int m_numRemainingPixels;
};

struct PickBodyArgs
{
    double m_rayFromWorld[3];
    double m_rayToWorld[3];
};


///Controlling a robot involves sending the desired state to its joint motor controllers.
///The control mode determines the state variables used for motor control.
struct SendDesiredStateArgs
{
	int m_bodyUniqueId;
	int m_controlMode;
	
	//PD parameters in case m_controlMode == CONTROL_MODE_POSITION_VELOCITY_PD
	double m_Kp[MAX_DEGREE_OF_FREEDOM];//indexed by degree of freedom, 6 for base, and then the dofs for each link
	double m_Kd[MAX_DEGREE_OF_FREEDOM];//indexed by degree of freedom, 6 for base, and then the dofs for each link
	double m_rhsClamp[MAX_DEGREE_OF_FREEDOM];

    int m_hasDesiredStateFlags[MAX_DEGREE_OF_FREEDOM];
    
	//desired state is only written by the client, read-only access by server is expected

	//m_desiredStateQ is indexed by position variables, 
	//starting with 3 base position variables, 4 base orientation variables (quaternion), then link position variables
    double m_desiredStateQ[MAX_DEGREE_OF_FREEDOM];
    

	//m_desiredStateQdot is index by velocity degrees of freedom, 3 linear and 3 angular variables for the base and then link velocity variables
    double m_desiredStateQdot[MAX_DEGREE_OF_FREEDOM];
	
	//m_desiredStateForceTorque is either the actual applied force/torque (in CONTROL_MODE_TORQUE) or
	//or the maximum applied force/torque for the PD/motor/constraint to reach the desired velocity in CONTROL_MODE_VELOCITY and CONTROL_MODE_POSITION_VELOCITY_PD mode
	//indexed by degree of freedom, 6 dof base, and then dofs for each link
    double m_desiredStateForceTorque[MAX_DEGREE_OF_FREEDOM];
    
};

enum EnumSimDesiredStateUpdateFlags
{
	SIM_DESIRED_STATE_HAS_Q=1,
	SIM_DESIRED_STATE_HAS_QDOT=2,
	SIM_DESIRED_STATE_HAS_KD=4,
	SIM_DESIRED_STATE_HAS_KP=8,
	SIM_DESIRED_STATE_HAS_MAX_FORCE=16,
	SIM_DESIRED_STATE_HAS_RHS_CLAMP=32
};


	

enum EnumSimParamUpdateFlags
{
	SIM_PARAM_UPDATE_DELTA_TIME=1,
	SIM_PARAM_UPDATE_GRAVITY=2,
	SIM_PARAM_UPDATE_NUM_SOLVER_ITERATIONS=4,	
	SIM_PARAM_UPDATE_NUM_SIMULATION_SUB_STEPS=8,
	SIM_PARAM_UPDATE_REAL_TIME_SIMULATION = 16,
	SIM_PARAM_UPDATE_DEFAULT_CONTACT_ERP=32,
	SIM_PARAM_UPDATE_INTERNAL_SIMULATION_FLAGS=64,
	SIM_PARAM_UPDATE_USE_SPLIT_IMPULSE=128,
	SIM_PARAM_UPDATE_SPLIT_IMPULSE_PENETRATION_THRESHOLD = 256,
	SIM_PARAM_UPDATE_COLLISION_FILTER_MODE=512,
	SIM_PARAM_UPDATE_CONTACT_BREAKING_THRESHOLD = 1024,
	SIM_PARAM_ENABLE_CONE_FRICTION = 2048,
	SIM_PARAM_ENABLE_FILE_CACHING = 4096,
	SIM_PARAM_UPDATE_RESTITUTION_VELOCITY_THRESHOLD = 8192,
	SIM_PARAM_UPDATE_DEFAULT_NON_CONTACT_ERP=16384,
	SIM_PARAM_UPDATE_DEFAULT_FRICTION_ERP = 32768,
};

enum EnumLoadBunnyUpdateFlags
{
    LOAD_BUNNY_UPDATE_SCALE=1,
    LOAD_BUNNY_UPDATE_MASS=2,
    LOAD_BUNNY_UPDATE_COLLISION_MARGIN=4
};

enum EnumSimParamInternalSimFlags
{
	SIM_PARAM_INTERNAL_CREATE_ROBOT_ASSETS=1,
};


///Controlling a robot involves sending the desired state to its joint motor controllers.
///The control mode determines the state variables used for motor control.

struct LoadBunnyArgs
{
    double m_scale;
    double m_mass;
    double m_collisionMargin;
};

struct RequestActualStateArgs
{
	int m_bodyUniqueId;
};

struct SendActualStateArgs
{
	int m_bodyUniqueId;
	int m_numLinks;
	int m_numDegreeOfFreedomQ;
	int m_numDegreeOfFreedomU;

    double m_rootLocalInertialFrame[7];
   
	  //actual state is only written by the server, read-only access by client is expected
    double m_actualStateQ[MAX_DEGREE_OF_FREEDOM];
    double m_actualStateQdot[MAX_DEGREE_OF_FREEDOM];

    //measured 6DOF force/torque sensors: force[x,y,z] and torque[x,y,z]
    double m_jointReactionForces[6*MAX_DEGREE_OF_FREEDOM];

    double m_jointMotorForce[MAX_DEGREE_OF_FREEDOM];
    
    double m_linkState[7*MAX_NUM_LINKS];
	double m_linkWorldVelocities[6*MAX_NUM_LINKS];//linear velocity and angular velocity in world space (x/y/z each).
    double m_linkLocalInertialFrames[7*MAX_NUM_LINKS];
};

struct b3SendCollisionInfoArgs
{
	int m_numLinks;
	double m_rootWorldAABBMin[3];
	double m_rootWorldAABBMax[3];
 
	double m_linkWorldAABBsMin[3*MAX_NUM_LINKS];
	double m_linkWorldAABBsMax[3*MAX_NUM_LINKS];
};

struct b3RequestCollisionInfoArgs
{
	int m_bodyUniqueId;
};


enum EnumSensorTypes
{
    SENSOR_FORCE_TORQUE=1,
    SENSOR_IMU=2,
};

struct CreateSensorArgs
{
    int m_bodyUniqueId;
    int m_numJointSensorChanges;
    int m_sensorType[MAX_DEGREE_OF_FREEDOM];
    
///todo: clean up the duplication, make sure no-one else is using those members directly (use C-API header instead)
    int m_jointIndex[MAX_DEGREE_OF_FREEDOM];
    int m_enableJointForceSensor[MAX_DEGREE_OF_FREEDOM];

    int m_linkIndex[MAX_DEGREE_OF_FREEDOM];
    int m_enableSensor[MAX_DEGREE_OF_FREEDOM];
    
};

typedef  struct SharedMemoryCommand SharedMemoryCommand_t;

enum EnumBoxShapeFlags
{
    BOX_SHAPE_HAS_INITIAL_POSITION=1,
    BOX_SHAPE_HAS_INITIAL_ORIENTATION=2,
    BOX_SHAPE_HAS_HALF_EXTENTS=4,
	BOX_SHAPE_HAS_MASS=8,
	BOX_SHAPE_HAS_COLLISION_SHAPE_TYPE=16,
	BOX_SHAPE_HAS_COLOR=32,
};
///This command will be replaced to allow arbitrary collision shape types
struct CreateBoxShapeArgs
{
    double m_halfExtentsX;
    double m_halfExtentsY;
    double m_halfExtentsZ;

	double m_mass;
	int m_collisionShapeType;//see SharedMemoryPublic.h

    double m_initialPosition[3];
	double m_initialOrientation[4];
	double m_colorRGBA[4];
};

struct b3ObjectArgs
{
    int m_numBodies;
    int m_bodyUniqueIds[MAX_SDF_BODIES];
	int m_numUserConstraints;
	int m_userConstraintUniqueIds[MAX_SDF_BODIES];
};

struct b3Profile
{
	char m_name[MAX_FILENAME_LENGTH];
	int m_durationInMicroSeconds;
};



struct SdfLoadedArgs
{
    int m_numBodies;
    int m_bodyUniqueIds[MAX_SDF_BODIES];
    int m_numUserConstraints;
	int m_userConstraintUniqueIds[MAX_SDF_BODIES];
    
    ///@todo(erwincoumans) load cameras, lights etc
    //int m_numCameras; 
    //int m_numLights; 
};


struct SdfRequestInfoArgs
{
    int m_bodyUniqueId;
};

///flags for b3ApplyExternalTorque and b3ApplyExternalForce
enum EnumExternalForcePrivateFlags
{
//    EF_LINK_FRAME=1,
//    EF_WORLD_FRAME=2,
    EF_TORQUE=4,
    EF_FORCE=8,
};



struct ExternalForceArgs
{
    int m_numForcesAndTorques;
    int m_bodyUniqueIds[MAX_SDF_BODIES];
    int m_linkIds[MAX_SDF_BODIES];
    double m_forcesAndTorques[3*MAX_SDF_BODIES];
    double m_positions[3*MAX_SDF_BODIES];
    int m_forceFlags[MAX_SDF_BODIES];
};

enum EnumSdfRequestInfoFlags
{
    SDF_REQUEST_INFO_BODY=1,
    //SDF_REQUEST_INFO_CAMERA=2,
};


struct CalculateInverseDynamicsArgs
{
	int m_bodyUniqueId;

	double m_jointPositionsQ[MAX_DEGREE_OF_FREEDOM];
	double m_jointVelocitiesQdot[MAX_DEGREE_OF_FREEDOM];
	double m_jointAccelerations[MAX_DEGREE_OF_FREEDOM];
};

struct CalculateInverseDynamicsResultArgs
{
	int m_bodyUniqueId;
	int m_dofCount;
	double m_jointForces[MAX_DEGREE_OF_FREEDOM];
};

struct CalculateJacobianArgs
{
    int m_bodyUniqueId;
    int m_linkIndex;
    double m_localPosition[3];
    double m_jointPositionsQ[MAX_DEGREE_OF_FREEDOM];
    double m_jointVelocitiesQdot[MAX_DEGREE_OF_FREEDOM];
    double m_jointAccelerations[MAX_DEGREE_OF_FREEDOM];
};

struct CalculateJacobianResultArgs
{
    int m_dofCount;
    double m_linearJacobian[3*MAX_DEGREE_OF_FREEDOM];
    double m_angularJacobian[3*MAX_DEGREE_OF_FREEDOM];
};

struct CalculateMassMatrixArgs
{
	int m_bodyUniqueId;
	double m_jointPositionsQ[MAX_DEGREE_OF_FREEDOM];
};

struct CalculateMassMatrixResultArgs
{
	int m_dofCount;
};

struct CalculateInverseKinematicsArgs
{
	int m_bodyUniqueId;
//	double m_jointPositionsQ[MAX_DEGREE_OF_FREEDOM];
	double m_targetPosition[3];
	double m_targetOrientation[4];//orientation represented as quaternion, x,y,z,w
	int m_endEffectorLinkIndex;
    double m_lowerLimit[MAX_DEGREE_OF_FREEDOM];
    double m_upperLimit[MAX_DEGREE_OF_FREEDOM];
    double m_jointRange[MAX_DEGREE_OF_FREEDOM];
    double m_restPose[MAX_DEGREE_OF_FREEDOM];
    double m_jointDamping[MAX_DEGREE_OF_FREEDOM];
};

struct CalculateInverseKinematicsResultArgs
{
	int m_bodyUniqueId;
	int m_dofCount;
	double m_jointPositions[MAX_DEGREE_OF_FREEDOM];
};

enum EnumUserConstraintFlags
{
    USER_CONSTRAINT_ADD_CONSTRAINT=1,
	USER_CONSTRAINT_REMOVE_CONSTRAINT=2,
	USER_CONSTRAINT_CHANGE_CONSTRAINT=4,
	USER_CONSTRAINT_CHANGE_PIVOT_IN_B=8,
	USER_CONSTRAINT_CHANGE_FRAME_ORN_IN_B=16,
	USER_CONSTRAINT_CHANGE_MAX_FORCE=32,
	USER_CONSTRAINT_REQUEST_INFO=64,
	USER_CONSTRAINT_CHANGE_GEAR_RATIO=128,	
	USER_CONSTRAINT_CHANGE_GEAR_AUX_LINK=256,
	USER_CONSTRAINT_CHANGE_RELATIVE_POSITION_TARGET=512,
	USER_CONSTRAINT_CHANGE_ERP=1024,
	USER_CONSTRAINT_REQUEST_STATE=2048,
};

enum EnumBodyChangeFlags
{
	BODY_DELETE_FLAG=1,
};




enum EnumUserDebugDrawFlags
{
    USER_DEBUG_HAS_LINE=1,
	USER_DEBUG_HAS_TEXT=2,
	USER_DEBUG_REMOVE_ONE_ITEM=4,
	USER_DEBUG_REMOVE_ALL=8,	
	USER_DEBUG_SET_CUSTOM_OBJECT_COLOR = 16,
	USER_DEBUG_REMOVE_CUSTOM_OBJECT_COLOR = 32,
	USER_DEBUG_ADD_PARAMETER=64,
	USER_DEBUG_READ_PARAMETER=128,
	USER_DEBUG_HAS_OPTION_FLAGS=256,
	USER_DEBUG_HAS_TEXT_ORIENTATION = 512,
	USER_DEBUG_HAS_PARENT_OBJECT=1024,
	USER_DEBUG_HAS_REPLACE_ITEM_UNIQUE_ID=2048,
};

struct UserDebugDrawArgs
{
	double	m_debugLineFromXYZ[3];
	double	m_debugLineToXYZ[3];
	double	m_debugLineColorRGB[3];
	double	m_lineWidth;
	
	double m_lifeTime;
	int m_itemUniqueId;

	char m_text[MAX_FILENAME_LENGTH];
	double m_textPositionXYZ[3];
	double m_textOrientation[4];
	int m_parentObjectUniqueId;
	int m_parentLinkIndex;
	double m_textColorRGB[3];
	double m_textSize;
	int m_optionFlags;
	int m_replaceItemUniqueId;

	double m_rangeMin;
	double m_rangeMax;
	double m_startValue;

	double m_objectDebugColorRGB[3];
	int m_objectUniqueId;
	int m_linkIndex;
};



struct UserDebugDrawResultArgs
{
	int m_debugItemUniqueId;
	double m_parameterValue;
};


struct SendVREvents
{
	int m_numVRControllerEvents;
	b3VRControllerEvent m_controllerEvents[MAX_VR_CONTROLLERS];
};

struct SendKeyboardEvents
{
	int m_numKeyboardEvents;
	b3KeyboardEvent m_keyboardEvents[MAX_KEYBOARD_EVENTS];
};

struct SendMouseEvents
{
	int m_numMouseEvents;
	b3MouseEvent m_mouseEvents[MAX_MOUSE_EVENTS];
};

enum eVRCameraEnums
{
	VR_CAMERA_ROOT_POSITION=1,
	VR_CAMERA_ROOT_ORIENTATION=2,
	VR_CAMERA_ROOT_TRACKING_OBJECT=4,
	VR_CAMERA_FLAG = 8,
};

enum eStateLoggingEnums
{
	STATE_LOGGING_START_LOG=1,
	STATE_LOGGING_STOP_LOG=2,
	STATE_LOGGING_FILTER_OBJECT_UNIQUE_ID=4,
	STATE_LOGGING_MAX_LOG_DOF=8,
	STATE_LOGGING_FILTER_LINK_INDEX_A=16,
	STATE_LOGGING_FILTER_LINK_INDEX_B=32,
	STATE_LOGGING_FILTER_BODY_UNIQUE_ID_A=64,
	STATE_LOGGING_FILTER_BODY_UNIQUE_ID_B=128,
	STATE_LOGGING_FILTER_DEVICE_TYPE=256,
	STATE_LOGGING_LOG_FLAGS=512
};

struct VRCameraState
{
	double m_rootPosition[3];
	double m_rootOrientation[4];
	int m_trackingObjectUniqueId;
	int m_trackingObjectFlag;
};



struct StateLoggingRequest
{
	char m_fileName[MAX_FILENAME_LENGTH];
	int m_logType;//Minitaur, generic robot, VR states, contact points
	int m_numBodyUniqueIds;////only if STATE_LOGGING_FILTER_OBJECT_UNIQUE_ID flag is set
	int m_bodyUniqueIds[MAX_SDF_BODIES];
	int m_loggingUniqueId;
	int m_maxLogDof;
	int m_linkIndexA; // only if STATE_LOGGING_FILTER_LINK_INDEX_A flag is set
	int m_linkIndexB; // only if STATE_LOGGING_FILTER_LINK_INDEX_B flag is set
	int m_bodyUniqueIdA; // only if STATE_LOGGING_FILTER_BODY_UNIQUE_ID_A flag is set
	int m_bodyUniqueIdB; // only if STATE_LOGGING_FILTER_BODY_UNIQUE_ID_B flag is set
	int m_deviceFilterType; //user to select (filter) which VR devices to log
	int m_logFlags;
};

struct StateLoggingResultArgs
{
	int m_loggingUniqueId;
};

enum InternalOpenGLVisualizerUpdateFlags
{
    COV_SET_CAMERA_VIEW_MATRIX=1,
    COV_SET_FLAGS=2,
};

struct ConfigureOpenGLVisualizerRequest
{
    double m_cameraDistance;
    double m_cameraPitch;
    double m_cameraYaw;
    double m_cameraTargetPosition[3];
  
    int m_setFlag;
    int m_setEnabled;
};

enum 
{
	URDF_GEOM_HAS_RADIUS = 1,
};

struct b3CreateUserShapeData
{
	int m_type;//see UrdfGeomTypes	

	int m_hasChildTransform;
	double m_childPosition[3];
	double m_childOrientation[4];

	double m_sphereRadius;
	double m_boxHalfExtents[3];	
	double m_capsuleRadius;
	double m_capsuleHeight;
	int		m_hasFromTo;
	double m_capsuleFrom[3];
	double m_capsuleTo[3];
	double m_planeNormal[3];
	double m_planeConstant;

	int         m_meshFileType;
	char		m_meshFileName[VISUAL_SHAPE_MAX_PATH_LEN];
	double		m_meshScale[3];
	int			m_collisionFlags;
	int			m_visualFlags;

	double		m_rgbaColor[4];
	double		m_specularColor[3];

};

#define MAX_COMPOUND_COLLISION_SHAPES 16

struct b3CreateUserShapeArgs
{
	int m_numUserShapes;
	b3CreateUserShapeData m_shapes[MAX_COMPOUND_COLLISION_SHAPES];
};

struct b3CreateUserShapeResultArgs
{
	int m_userShapeUniqueId;
};


#define MAX_CREATE_MULTI_BODY_LINKS 128
enum eCreateMultiBodyEnum
{
	MULTI_BODY_HAS_BASE=1,
	MULT_BODY_USE_MAXIMAL_COORDINATES=2,
};
struct b3CreateMultiBodyArgs
{
	char m_bodyName[1024];
	int m_baseLinkIndex;

	double m_linkPositions[3*MAX_CREATE_MULTI_BODY_LINKS];
	double m_linkOrientations[4*MAX_CREATE_MULTI_BODY_LINKS];

	int m_numLinks;
	double m_linkMasses[MAX_CREATE_MULTI_BODY_LINKS];
	double m_linkInertias[MAX_CREATE_MULTI_BODY_LINKS*3];

	double m_linkInertialFramePositions[MAX_CREATE_MULTI_BODY_LINKS*3];
	double m_linkInertialFrameOrientations[MAX_CREATE_MULTI_BODY_LINKS*4];

	int m_linkCollisionShapeUniqueIds[MAX_CREATE_MULTI_BODY_LINKS];
	int m_linkVisualShapeUniqueIds[MAX_CREATE_MULTI_BODY_LINKS];
	int m_linkParentIndices[MAX_CREATE_MULTI_BODY_LINKS];
	int m_linkJointTypes[MAX_CREATE_MULTI_BODY_LINKS];
	double m_linkJointAxis[3*MAX_CREATE_MULTI_BODY_LINKS];

	#if 0
	std::string m_name;
	std::string m_sourceFile;
    btTransform m_rootTransformInWorld;
	btHashMap<btHashString, UrdfMaterial*> m_materials;
	btHashMap<btHashString, UrdfLink*> m_links;
	btHashMap<btHashString, UrdfJoint*> m_joints;
	#endif
};

struct b3CreateMultiBodyResultArgs
{
	int m_bodyUniqueId;
};

struct b3ChangeTextureArgs
{
	int m_textureUniqueId;
	int m_width;
	int m_height;
};

struct b3StateSerializationArguments
{
	char m_fileName[MAX_URDF_FILENAME_LENGTH];
	int m_stateId;
};

struct SharedMemoryCommand
{
	int m_type;
	smUint64_t	m_timeStamp;
	int	m_sequenceNumber;
	
	//m_updateFlags is a bit fields to tell which parameters need updating
    //for example m_updateFlags = SIM_PARAM_UPDATE_DELTA_TIME | SIM_PARAM_UPDATE_NUM_SOLVER_ITERATIONS;
    int m_updateFlags;

    union
    {
        struct UrdfArgs m_urdfArguments;
		struct SdfArgs m_sdfArguments;
		struct MjcfArgs	m_mjcfArguments;
		struct FileArgs m_fileArguments;
		struct SdfRequestInfoArgs m_sdfRequestInfoArgs;
		struct ChangeDynamicsInfoArgs m_changeDynamicsInfoArgs;
		struct GetDynamicsInfoArgs m_getDynamicsInfoArgs;
		struct InitPoseArgs m_initPoseArgs;
		struct b3PhysicsSimulationParameters m_physSimParamArgs;
		struct BulletDataStreamArgs	m_dataStreamArguments;
		struct SendDesiredStateArgs m_sendDesiredStateCommandArgument;
		struct RequestActualStateArgs m_requestActualStateInformationCommandArgument;
        struct CreateSensorArgs m_createSensorArguments;
        struct CreateBoxShapeArgs m_createBoxShapeArguments;
		struct RequestDebugLinesArgs m_requestDebugLinesArguments;
		struct RequestPixelDataArgs m_requestPixelDataArguments;
		struct PickBodyArgs m_pickBodyArguments;
        struct ExternalForceArgs m_externalForceArguments;
		struct CalculateInverseDynamicsArgs m_calculateInverseDynamicsArguments;
        struct CalculateJacobianArgs m_calculateJacobianArguments;
        struct CalculateMassMatrixArgs m_calculateMassMatrixArguments;
        struct b3UserConstraint m_userConstraintArguments;
        struct RequestContactDataArgs m_requestContactPointArguments;
		struct RequestOverlappingObjectsArgs m_requestOverlappingObjectsArgs;
        struct RequestVisualShapeDataArgs m_requestVisualShapeDataArguments;
        struct UpdateVisualShapeDataArgs m_updateVisualShapeDataArguments;
        struct LoadTextureArgs m_loadTextureArguments;
		struct CalculateInverseKinematicsArgs m_calculateInverseKinematicsArguments;
		struct UserDebugDrawArgs m_userDebugDrawArgs;
		struct RequestRaycastIntersections m_requestRaycastIntersections;
        struct LoadBunnyArgs m_loadBunnyArguments;
		struct VRCameraState m_vrCameraStateArguments;
		struct StateLoggingRequest m_stateLoggingArguments;
        struct ConfigureOpenGLVisualizerRequest m_configureOpenGLVisualizerArguments;
		struct b3ObjectArgs m_removeObjectArgs;
		struct b3Profile m_profile;
		struct b3CreateUserShapeArgs m_createUserShapeArgs;
		struct b3CreateMultiBodyArgs m_createMultiBodyArgs;
		struct b3RequestCollisionInfoArgs m_requestCollisionInfoArgs;
		struct b3ChangeTextureArgs m_changeTextureArgs;
		struct b3SearchPathfArgs m_searchPathArgs;
		struct b3CustomCommand m_customCommandArgs;
		struct b3StateSerializationArguments m_loadStateArguments;
		struct RequestCollisionShapeDataArgs m_requestCollisionShapeDataArguments;		
    };
};

struct RigidBodyCreateArgs
{
	int m_bodyUniqueId; 
};

struct SendContactDataArgs
{
    int m_startingContactPointIndex;
    int m_numContactPointsCopied;
    int m_numRemainingContactPoints;
};

struct SendOverlappingObjectsArgs
{
	int m_startingOverlappingObjectIndex;
	int m_numOverlappingObjectsCopied;
	int m_numRemainingOverlappingObjects;
};






struct SharedMemoryStatus
{
	int m_type;
	
	smUint64_t	m_timeStamp;
	int	m_sequenceNumber;
	
	//m_streamBytes is only for internal purposes
	int		m_numDataStreamBytes;
	char*	m_dataStream;

	//m_updateFlags is a bit fields to tell which parameters were updated, 
	//m_updateFlags is ignored for most status messages
    int m_updateFlags;

	union
	{
		struct BulletDataStreamArgs	m_dataStreamArguments;
		struct SdfLoadedArgs m_sdfLoadedArgs;
		struct SendActualStateArgs m_sendActualStateArgs;
		struct SendDebugLinesArgs m_sendDebugLinesArgs;
		struct SendPixelDataArgs m_sendPixelDataArguments;
		struct RigidBodyCreateArgs m_rigidBodyCreateArgs;
		struct CalculateInverseDynamicsResultArgs m_inverseDynamicsResultArgs;
        struct CalculateJacobianResultArgs m_jacobianResultArgs;
        struct CalculateMassMatrixResultArgs m_massMatrixResultArgs;
		struct SendContactDataArgs m_sendContactPointArgs;
		struct SendOverlappingObjectsArgs m_sendOverlappingObjectsArgs;
		struct CalculateInverseKinematicsResultArgs m_inverseKinematicsResultArgs;
		struct SendVisualShapeDataArgs m_sendVisualShapeArgs;
		struct UserDebugDrawResultArgs m_userDebugDrawArgs;
		struct b3UserConstraint m_userConstraintResultArgs;
		struct b3UserConstraintState m_userConstraintStateResultArgs;
		struct SendVREvents m_sendVREvents;
		struct SendKeyboardEvents m_sendKeyboardEvents;
		struct SendRaycastHits m_raycastHits;
		struct StateLoggingResultArgs m_stateLoggingResultArgs;
		struct b3OpenGLVisualizerCameraInfo m_visualizerCameraResultArgs;
		struct b3ObjectArgs m_removeObjectArgs;
		struct b3DynamicsInfo m_dynamicsInfo;
		struct b3CreateUserShapeResultArgs m_createUserShapeResultArgs;
		struct b3CreateMultiBodyResultArgs m_createMultiBodyResultArgs;
		struct b3SendCollisionInfoArgs m_sendCollisionInfoArgs;
		struct SendMouseEvents m_sendMouseEvents;
		struct b3LoadTextureResultArgs m_loadTextureResultArguments;
		struct b3CustomCommandResultArgs m_customCommandResultArgs;
		struct b3PhysicsSimulationParameters m_simulationParameterResultArgs;
		struct b3StateSerializationArguments m_saveStateResultArgs;
		struct SendCollisionShapeDataArgs m_sendCollisionShapeArgs;
	};
};

typedef  struct SharedMemoryStatus SharedMemoryStatus_t;



#endif //SHARED_MEMORY_COMMANDS_H
