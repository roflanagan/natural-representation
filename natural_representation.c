#include <stdio.h>
#include <math.h>
#include <string.h>
#include <sys/time.h>
#include <stdlib.h>

void continued_fraction(unsigned long numerator, unsigned long denominator, int *sequence, int *i)
{
    unsigned long new_numerator;
    *i = 0;
    
    while (denominator > 1)
    {
        sequence[*i] = numerator / denominator;
        new_numerator = numerator - sequence[*i] * denominator;
        numerator = denominator;
        denominator = new_numerator;
        *i = *i + 1;
    }
    sequence[*i] = numerator;
    *i = *i + denominator;
}

void evaluate_continued_fraction(unsigned long *numerator, unsigned long *denominator, 
                                 int *sequence, int *sequence_size)
{
    unsigned long old_numerator;
    int i = *sequence_size - 1;
    *numerator = sequence[i];
    *denominator = 1;
    
    while (i > 0)
    {
        i -= 1;
        old_numerator = *numerator;
        *numerator = *denominator + sequence[i] * *numerator;
        *denominator = old_numerator;
    }
}

void natural_representation(unsigned long numerator, unsigned long denominator, int *sequence, int *i)
{
    int sign = 1;
    unsigned long integer_part, fractional_part, old_denominator;
    *i = 0;

    while (1)
    {
        integer_part = numerator / denominator;
        fractional_part = numerator - integer_part * denominator;
        sequence[*i] = sign * (integer_part + (fractional_part > 0));
        *i = *i + 1;
        if (2 * fractional_part >= denominator)
        {
            denominator = denominator - fractional_part;
            numerator = fractional_part - denominator;
        }
        else
        {
            if (fractional_part == 0)
                return;
            old_denominator = denominator;
            denominator = fractional_part;
            numerator = old_denominator - 2 * fractional_part;
            sign *= -1;
        }
        
    }
}

void evaluate_natural_representation(unsigned long *numerator, unsigned long *denominator, 
                                     int *sequence, int *sequence_size)
{
    unsigned long new_denominator, old_numerator;
    int i = *sequence_size - 1, previous_sign = (sequence[i] >= 0);
    *numerator = abs(sequence[i]);
    *denominator = 1;
 
    while (i > 0)
    {
        i -= 1;
        old_numerator = *numerator;
        new_denominator = old_numerator + 2 * *denominator;
        *numerator = abs(sequence[i]) * new_denominator - *denominator;
        
        if ((sequence[i] < 0) == previous_sign)
        {
            *numerator -= old_numerator;
            previous_sign = 1 - previous_sign;
        }
        *denominator = new_denominator;
    }
}

unsigned long current_time()
{
    struct timeval tv;
    gettimeofday(&tv,NULL);
    return 1000000 * tv.tv_sec + tv.tv_usec;
}

void repeatedly_construct_continued_fraction(unsigned long numerator, 
                                             unsigned long denominator, 
                                             int *sequence, int *sequence_size, int iterations)
{
    long start, i;
    printf("continued fraction:\n");
    
    start = current_time();
    for (i = 0; i < iterations; i++)
        continued_fraction(numerator, denominator, sequence, sequence_size);

    printf("completed in %ld microseconds\n", current_time()-start);

    for (i=0 ; i < *sequence_size; i++)
        printf("%d, ", sequence[i]);
    printf("\n");
}

void repeatedly_evaluate_continued_fraction(unsigned long numerator, 
                                            unsigned long denominator, 
                                            int *sequence, int *sequence_size, int iterations)
{
    long start, i;
    printf("\n\nevaluation of continued fraction:\n");
    
    start = current_time();
    for (i = 0; i < iterations; i++)
        evaluate_continued_fraction(&numerator, &denominator, sequence, sequence_size);

    printf("completed in %ld microseconds\n", current_time()-start);
    printf("numerator: %lu   denominator: %lu\n\n", numerator, denominator);
}

void repeatedly_construct_natural_representation(unsigned long numerator, 
                                                 unsigned long denominator, 
                                                 int *sequence, int *sequence_size, 
                                                 int iterations)
{
    long start, i;

    printf("\n\n\nnatural representation:\n");
    
    start = current_time();
    for (i = 0; i < iterations; i++)
        natural_representation(numerator, denominator, sequence, sequence_size);
    
    printf("completed in %ld microseconds\n", current_time()-start);

    for (i=0 ; i < *sequence_size; i++)
        printf("%d, ", sequence[i]);
    printf("\n\n");
}

void repeatedly_evaluate_natural_representation(unsigned long numerator, 
                                                unsigned long denominator, 
                                                int *sequence, int *sequence_size,
                                                int iterations)
{
    long start, i;

    printf("\n\nevaluation of natural representation:\n");
    
    start = current_time();
    for (i = 0; i < iterations; i++)
        evaluate_natural_representation(&numerator, &denominator, sequence, sequence_size);

    printf("completed in %ld microseconds\n", current_time()-start);
    printf("numerator: %lu   denominator: %lu\n\n", numerator, denominator);
}

int main(int argc, char **argv)
{
    unsigned long numerator, denominator;
    int sequence[BUFSIZ], sequence_size, iterations = 10000000;

    if (argc < 3)
    {
        printf("Usage: %s numerator denominator\n", argv[0]);
        return 0;
    }
    sscanf(argv[1], "%lu", &numerator);
    sscanf(argv[2], "%lu", &denominator);

    printf("numerator: %lu   denominator: %lu\n\n", numerator, denominator);
    
    repeatedly_construct_continued_fraction(numerator, denominator, sequence, &sequence_size, iterations);
    repeatedly_evaluate_continued_fraction(numerator, denominator, sequence, &sequence_size, iterations);

    repeatedly_construct_natural_representation(numerator, denominator, sequence, &sequence_size, iterations);
    repeatedly_evaluate_natural_representation(numerator, denominator, sequence, &sequence_size, iterations);
}