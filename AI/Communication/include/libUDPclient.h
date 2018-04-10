#ifndef UDPCLIENT_H
#define UDPCLIENT_H

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <ctype.h>
#include <string.h>
#include <netdb.h>

#define Struct2String(x) ((char*)&x)

class UDPClient
{
public:
    UDPClient();
    UDPClient(char* address_port, char *protocol);
    virtual ~UDPClient();

    bool Initilaize(char *address_port, char *protocol);

    bool receive(char *data, uint length);
    bool receive(char *data);
    char* receive(uint length);

    bool send(const char *data, uint length);

    //==========NOTE : must be can determined the length of data----------------
//    bool send(const char *data);

//    const UDPClient& operator << ( const char* &);
//    const UDPClient& operator << ( const int);
//    const UDPClient& operator >> ( void*);

private:
    int z;
    uint x;
    struct sockaddr_in adr;  /* AF_INET */
    int len_inet;            /* length */
    int s;                   /* Socket */
    static int so_reuseaddr;

    bool displayError(const char *on_what);
    int mkaddr(void *addr,
               int *addrlen,
               char *str_addr,
               char *protocol);
};

//FEATURE : DOXYGEN documentation
/*! \class UDPClient
 *\brief Class for Client Socket
 * This class is for connecting to a server using format IP:Port. */

/*! \fn int Initilaize(char* address_port)
 *  \brief Initialize what host and port to be connected
 *  \param address_port a hostname and port number. Example: localhost:8080
 *  \return 1 if success \n 0 if failed.
 */

#endif // UDPCLIENT_H
