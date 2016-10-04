#include "libUDPclient.h"

int UDPClient::so_reuseaddr = 1;

UDPClient::UDPClient()
{
}

UDPClient::UDPClient(char *address_port, char *protocol)
{
    Initilaize(address_port, protocol);
}

UDPClient::~UDPClient()
{
}

bool UDPClient::Initilaize(char *address_port, char *protocol)
{
    /*
    * Create a UDP socket to use:
    */
    s = socket(AF_INET,SOCK_DGRAM,0);
    if ( s == -1 )
        return displayError("socket()");

    /*
    * Form the broadcast address:
    */
    len_inet = sizeof adr;

    z = mkaddr(&adr,
               &len_inet,
               address_port,
               protocol);

    if ( z == -1 )
        return displayError("Bad broadcast address");

    /*
    * Allow multiple listeners on the
    * broadcast address:
    */
    z = setsockopt(s,
                   SOL_SOCKET,
                   SO_REUSEADDR,
                   &so_reuseaddr,
                   sizeof so_reuseaddr);

    if ( z == -1 )
        return displayError("setsockopt(SO_REUSEADDR)");

    /*
    * Bind our socket to the broadcast address:
    */
    z = bind(s,
             (struct sockaddr *)&adr,
             len_inet);

    if ( z == -1 )
        return displayError("bind(2)");

    return true;
}

bool UDPClient::receive(char *data, uint length)
{
    z = recvfrom(s,      /* Socket */
                 data,  /* Receiving buffer */
                 length,/* Max rcv buf size */
                 0,      /* Flags: no options */
                 (struct sockaddr *)&adr, /* Addr */
                 &x);    /* Addr len, in & out */

    if ( z < 0 )
        return displayError("recvfrom(2)"); /* else err */
}

bool UDPClient::receive(char *data)
{
    receive(data, sizeof(*data));
//    z = recvfrom(s,      /* Socket */
//                 data,  /* Receiving buffer */
//                 sizeof(*data),/* Max rcv buf size */
//                 0,      /* Flags: no options */
//                 (struct sockaddr *)&adr, /* Addr */
//                 &x);    /* Addr len, in & out */

//    if ( z < 0 )
//        return displayError("recvfrom(2)"); /* else err */
}

char *UDPClient::receive(uint length)
{
    static char* data;
    z = recvfrom(s,      /* Socket */
                 data,  /* Receiving buffer */
                 length,/* Max rcv buf size */
                 0,      /* Flags: no options */
                 (struct sockaddr *)&adr, /* Addr */
                 &x);    /* Addr len, in & out */

    if ( z < 0 )
        return NULL;
    else
        return data;
}

bool UDPClient::send(const char *data, uint length)
{
    z = sendto(s,      /* Socket */
               data,  /* Receiving buffer */
               length,/* Max rcv buf size */
               0,      /* Flags: no options */
               (const struct sockaddr *)&adr, /* Addr */
               sizeof(adr));    /* Addr len, in & out */

    if ( z < 0 )
        return displayError("recvfrom(2)"); /* else err */
}


int UDPClient::mkaddr(void *addr, int *addrlen, char *str_addr, char *protocol)
{
    char *inp_addr = strdup(str_addr);
    char *host_part = strtok(inp_addr, ":" );
    char *port_part = strtok(NULL, "\n" );
    struct sockaddr_in *ap =
            (struct sockaddr_in *) addr;
            struct hostent *hp = NULL;
            struct servent *sp = NULL;
            char *cp;
            long lv;

            // /*
            //  * Set input defaults:
            //  */
            //  if ( !host_part ) {
            //    host_part =  "*" ;
            //  }
            //  if ( !port_part ) {
            //    port_part =  "*" ;
            //  }
            //  if ( !protocol ) {
            //    protocol =  "tcp" ;
            //  }

            /*
    * Initialize the address structure:
    */
            memset(ap,0,*addrlen);
            ap->sin_family = AF_INET;
            ap->sin_port = 0;
            ap->sin_addr.s_addr = INADDR_ANY;

            /*
    * Fill in the host address:
    */
            if ( strcmp(host_part, "*" ) == 0 ) {
                ; /* Leave as INADDR_ANY */
            }
            else if ( isdigit(*host_part) ) {
                /*
      * Numeric IP address:
      */
                ap->sin_addr.s_addr =
                        inet_addr(host_part);
                // if ( ap->sin_addr.s_addr == INADDR_NONE ) {
                if ( !inet_aton(host_part,&ap->sin_addr) ) {
                    return -1;
                }
            }
            else {
                /*
    * Assume a hostname:
    */
                hp = gethostbyname(host_part);
                if ( !hp ) {
                    return -1;
                }
                if ( hp->h_addrtype != AF_INET ) {
                    return -1;
                }
                ap->sin_addr = * (struct in_addr *)
                        hp->h_addr_list[0];
            }

            /*
    * Process an optional port #:
    */
            if ( !strcmp(port_part, "*" ) ) {
                /* Leave as wild (zero) */
            }
            else if ( isdigit(*port_part) ) {
                /*
    * Process numeric port #:
    */
                lv = strtol(port_part,&cp,10);
                if ( cp != NULL && *cp ) {
                    return -2;
                }
                if ( lv < 0L || lv >= 32768 ) {
                    return -2;
                }
                ap->sin_port = htons( (short)lv);
            }
            else {
                /*
    * Lookup the service:
    */
                sp = getservbyname( port_part, protocol);
                if ( !sp ) {
                    return -2;
                }
                ap->sin_port = (short) sp->s_port;
            }

            /*
    * Return address length
    */
            *addrlen = sizeof *ap;

            free(inp_addr);
            return 0;
}


bool UDPClient::displayError(const char *on_what)
{
    fputs(strerror(errno),stdout);
    fputs(": ",stdout);
    fputs(on_what,stdout);
    fputc('\n',stdout);
    return false;
}


//const UDPClient& UDPClient::operator >>(void *data)
//{
//    receive((char*)data, sizeof(data));
//    return *this;
//}

//const UDPClient &UDPClient::operator <<(const char* &data)
//{
//    send(data, sizeof(data));
//}

//const UDPClient &UDPClient::operator <<(const int data)
//{
//    send((char*) data, sizeof(data));
//}
