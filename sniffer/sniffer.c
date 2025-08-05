#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <netpacket/packet.h>
#include <time.h>
#include <jansson.h>  // Install with: sudo apt-get install libjansson-dev

void process_packet(unsigned char*, int);

int main(int argc, char *argv[]) {
    // ... (existing socket setup code)

    // Interface selection
    char *interface = NULL;
    if (argc > 2 && strcmp(argv[1], "-i") == 0) {
        interface = argv[2];
    }

    // ... (rest of main capture loop)
}

void process_packet(unsigned char *buffer, int size) {
    struct ethhdr *eth = (struct ethhdr *)buffer;
    struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));
    
    // Only process IP packets
    if (eth->h_proto != htons(ETH_P_IP)) 
        return;

    struct sockaddr_in source, dest;
    memset(&source, 0, sizeof(source));
    memset(&dest, 0, sizeof(dest));
    source.sin_addr.s_addr = iph->saddr;
    dest.sin_addr.s_addr = iph->daddr;

    // Create JSON object
    json_t *root = json_object();
    json_object_set_new(root, "time", json_integer(time(NULL)));
    json_object_set_new(root, "src_ip", json_string(inet_ntoa(source.sin_addr)));
    json_object_set_new(root, "dst_ip", json_string(inet_ntoa(dest.sin_addr)));
    
    char *protocol_str;
    switch (iph->protocol) {
        case IPPROTO_ICMP: 
            protocol_str = "ICMP";
            break;
        case IPPROTO_TCP:
            protocol_str = "TCP";
            // Add TCP ports
            struct tcphdr *tcph = (struct tcphdr*)(buffer + sizeof(struct ethhdr) + iph->ihl*4);
            json_object_set_new(root, "src_port", json_integer(ntohs(tcph->source)));
            json_object_set_new(root, "dst_port", json_integer(ntohs(tcph->dest)));
            break;
        case IPPROTO_UDP:
            protocol_str = "UDP";
            // Add UDP ports
            struct udphdr *udph = (struct udphdr*)(buffer + sizeof(struct ethhdr) + iph->ihl*4);
            json_object_set_new(root, "src_port", json_integer(ntohs(udph->source)));
            json_object_set_new(root, "dst_port", json_integer(ntohs(udph->dest)));
            break;
        default:
            protocol_str = "Other";
    }
    json_object_set_new(root, "protocol", json_string(protocol_str));

    // Print JSON to stdout
    char *json_str = json_dumps(root, JSON_COMPACT);
    printf("%s\n", json_str);
    fflush(stdout);
    
    // Cleanup
    free(json_str);
    json_decref(root);
}
