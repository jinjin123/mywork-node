#include < windows.h >
#include < stdio.h >

#define SLEEP_TIME 5000
#define LOGFILE "C:\\MyServices\\memstatus.txt"


int WriteToLog(char* str)
{
    FILE* log;
    log = fopen(LOGFILE, "a+");
    if (log == NULL)
    return -1;
    fprintf(log, "%s\n", str);
    fclose(log);
    return 0;
}

SERVICE_STATUS ServiceStatus;
SERVICE_STATUS_HANDLE hStatus;
void ServiceMain(int argc, char** argv);
void ControlHandler(DWORD request);
int InitService();

void main()
{
    SERVICE_TABLE_ENTRY ServiceTable[2];
    ServiceTable[0].lpServiceName = "MemoryStatus";
    ServiceTable[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTION)ServiceMain;
 
    ServiceTable[1].lpServiceName = NULL;
    ServiceTable[1].lpServiceProc = NULL;

// 启动服务的控制分派机线程
    StartServiceCtrlDispatcher(ServiceTable);
}

error = InitService();
if (error)
{
// 初始化失败，终止服务
   ServiceStatus.dwCurrentState = SERVICE_STOPPED;
   ServiceStatus.dwWin32ExitCode = -1;
   SetServiceStatus(hStatus, &ServiceStatus);
   // 退出 ServiceMain
   return;
}


