

#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "md5.c"

int buff1[32], buff2[32];
uint64_t high, low;

int fakelcs(char const * const left, char const * const right)
{
    int i, j;
    int max = 0;

    int *curr = buff1;
    int *prev = buff2;
    int *swap = NULL;

    memset(curr, 0, 32);
    memset(prev, 0, 32);

    for(i = 0; i < 26; ++i)
    {
        for(j = 0; j < 26; ++j)
        {
            if(left[i] != right[j])
            {
                curr[j] = 0;
            }
            else
            {
                if(i != 0 && j != 0)
                {
                    curr[j] = 1 + prev[j-1];
                }
                else
                {
                    curr[j] = 1;
                }
                if(max < curr[j])
                {
                    max = curr[j];
                }
            }
        }
        swap = curr;
        curr = prev;
        prev = swap;
    }

    return max;
}


int lcs(char const * const left, char const * const right)
{
    int i, j;
    int max = 0;

    int *curr = buff1;
    int *prev = buff2;
    int *swap = NULL;

    memset(curr, 0, 32);
    memset(prev, 0, 32);

    for(i = 0; i < 32; ++i)
    {
        for(j = 0; j < 32; ++j)
        {
            if(left[i] != right[j])
            {
                curr[j] = 0;
            }
            else
            {
                if(i == 0 || j == 0)
                {
                    curr[j] = 1;
                }
                else
                {
                    curr[j] = 1 + prev[j-1];
                }
                if(max < curr[j])
                {
                    max = curr[j];
                }
            }
        }
        swap = curr;
        curr = prev;
        prev = swap;
    }

    return max;
}

#ifdef BENCHMARK
int check_compile()
{
    char one[33] = "d566bf2059f2882deb6d418aed0f0471";
    char two[33];

    md5_state_t state;
    md5_byte_t digest[16];

    md5_init(&state);
    md5_append(&state, (const md5_byte_t *)one, 32);
    md5_finish(&state, digest);

    sprintf(two, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x", digest[0], digest[1], digest[2], digest[3], digest[4], digest[5], digest[6], digest[7], digest[8], digest[9], digest[10], digest[11], digest[12], digest[13], digest[14], digest[15]);

    if(lcs(one, two) != 13)
        return 1;

    return 0;
}
#endif

void *reporting(void *ignore)
{
#ifdef BENCHMARK
    int bcounts = 0;
#endif
    uint64_t start_low;
    start_low = low;
    while(1)
    {
        uint64_t cur_low;
        
        sleep(5);

        cur_low = low;

        if(cur_low < start_low) continue;

#ifdef BENCHMARK
        fprintf(stderr, "%lu\n", (cur_low-start_low)/5000);
#else
        fprintf(stderr, "Processing %luK a second\n", (cur_low-start_low)/5000);
#endif
        start_low = cur_low;

#ifdef BENCHMARK
        bcounts++;
        if(bcounts > 4)
            exit(0);
#endif
    }
    return NULL;

}

int main(int argc, char *argv[])
{
    uint64_t prev_low = 0;
    pthread_t id;
    FILE *fp;

    char one[33];
    char two[33];

    srand(time(NULL));

    high = (((uint64_t)rand())<<32) | rand();
    low = (((uint64_t)rand())<<32) | rand();

    fp = fopen("progress.txt", "a");

#ifdef BENCHMARK
    if(check_compile())
    {
        return 1;
    }
#endif

    pthread_create(&id, 0, reporting, NULL);

    while(1)
    {
        md5_state_t state;
        md5_byte_t digest[16];
        int common = 0;

        sprintf(one, "%016lx%016lx", high, low);

        md5_init(&state);
        md5_append(&state, (const md5_byte_t *)one, 32);
        md5_finish(&state, digest);

        sprintf(two, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x", digest[0], digest[1], digest[2], digest[3], digest[4], digest[5], digest[6], digest[7], digest[8], digest[9], digest[10], digest[11], digest[12], digest[13], digest[14], digest[15]);

        common = fakelcs(one, two);

        if(common > 5)
        {
            common = lcs(one, two);
            if(common > 11)
            {
                fprintf(fp, "%s %s %d\n", one, two, common);
                fflush(fp);
            }
        }

        prev_low = low;
        ++low;
        if(low < prev_low) ++high;
    }

    return 0;
    
}
