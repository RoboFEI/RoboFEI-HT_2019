#ifndef THREADING_H
#define THREADING_H

#include <pthread.h>
#include <string.h>

bool thread_start;

void threadInitialize(pthread_t &thread, void *(*start_routine)(void *), int priority)
{
    int error;
    struct sched_param param;
    pthread_attr_t attr;

    pthread_attr_init(&attr);

    error = pthread_attr_setschedpolicy(&attr, SCHED_RR);
    if(error != 0)
        printf("error = %d\n",error);

    error = pthread_attr_setinheritsched(&attr, PTHREAD_INHERIT_SCHED);
    if(error != 0)
        printf("error = %d\n",error);

    memset(&param, 0, sizeof(param));
    param.sched_priority = priority;
    error = pthread_attr_setschedparam(&attr, &param);
    if(error != 0)
        printf("error = %d\n",error);

    thread_start = true;
    error = pthread_create(&thread, &attr, start_routine, NULL);
    if(error != 0)
        printf("error = %d\n",error);
}

#endif // THREADING_H
