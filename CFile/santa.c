#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

float cities[197769][4];
// cityId, x, y, isPrime;

int bestPath[197770];
int primeNum = 0;
int primeUsed = 0;
double bestScore = 999999;

int checkPrime(int a);
void loadCities();
void loadPath();
double calcDistance();
void countUsedPrime();
void swapPath();
void primeMover();
void shuffle(int ary[], int size);
void randomOptimizer(int range);
double calcShortDistance(int start, int end);
void randomDistOptimizer();
void outputCSV();

    int main()
{
    double distance = 0;
    loadCities();
    loadPath();
    distance = calcDistance();
    bestScore = distance;
    printf("distance: %lf\n", distance);
    printf("Prime: %d\n", primeNum);
    countUsedPrime();
    printf("\n");
    // primeMover();
    while(1512800 < bestScore){
        randomOptimizer(rand() % 3 + 4);
        //randomDistOptimizer();
        distance = calcDistance();
        printf("distance: %lf\n", distance);
        countUsedPrime();
        outputCSV();
    }
    printf("\n");
}

void loadCities(){
    FILE *fp;
    char *fname = "cities.csv";
    int ret;
    char buf[3][10];

    fp = fopen(fname, "r");
    if (fp == NULL)
    {
        printf("%sファイルが開けません\n", fname);
    }

    printf("\n");

    fscanf(fp, "%[^,],%[^,],%s", buf[0], buf[1], buf[2]);
    printf("%s %s %s\n", buf[0], buf[1], buf[2]);
    int i = 0;
    while ((ret = fscanf(fp, "%f,%f,%f", &cities[i][0], &cities[i][1], &cities[i][2])) != EOF)
    {
        cities[i][3] = checkPrime(cities[i][0]);
        if (cities[i][3] == 1){
            primeNum += 1;
        }
        printf("%.0f %f %f %f\n", cities[i][0], cities[i][1], cities[i][2], cities[i][3]);
        i++;
    }
    printf("\n");
    fclose(fp);
}

void loadPath()
{
    FILE *fp;
    char *fname = "submission.csv";
    int ret;
    char buf[10];

    fp = fopen(fname, "r");
    if (fp == NULL)
    {
        printf("%sファイルが開けません\n", fname);
    }

    printf("\n");

    fscanf(fp, "%s", buf);
    printf("%s\n", buf);
    int i = 0;
    while ((ret = fscanf(fp, "%d", &bestPath[i])) != EOF)
    {
        printf("%d\n", bestPath[i]);
        i++;
    }
    printf("\n");
    fclose(fp);
}

double calcDistance(){
    double distance = 0;
    double x1 ,x2 ,y1 ,y2;
    int usedPrime = 0;
    for (int i = 0; i < 197769; i++){
        x1 = cities[bestPath[i]][1], y1 = cities[bestPath[i]][2];
        x2 = cities[bestPath[i + 1]][1], y2 = cities[bestPath[i + 1]][2];
        if (i % 10 == 9 && cities[bestPath[i]][3] != 1){
            distance += pow((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1), 0.5) * 1.1;
        }else{
            distance += pow((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1), 0.5);
        }
    }
    return distance;
}

int checkPrime(int a){
    int c;

    for (c = 2; c <= a - 1; c++){
        if (a % c == 0){
            break;
        }
    }
    if (c == a){
        return 1;
    }else{
        return 0;
    }
}

void countUsedPrime(){
    int usedPrime = 0;
    for (int i = 9; i < 197769; i+=10){
        if (cities[bestPath[i]][3] == 1){
            usedPrime++;
        }
    }
    printf("%d\n",usedPrime);
    primeUsed = usedPrime;
    printf("Used: %d\n", primeUsed);
}

void swapPath(int a, int b){
    int temp = bestPath[a];
    bestPath[a] = bestPath[b];
    bestPath[b] = temp;
}

void primeMover(){
    int j;
    int mod;
    for (int i = 0; i < 197769; i++){
        mod = i % 10;
        if (mod != 9 && cities[bestPath[i]][3] == 1){
            if(mod <=  5){
                j = i - (i % 10) - 1;
            }else{
                j = i + 9 - (i % 10);
            }
            if (cities[bestPath[j]][3] != 1){
                swapPath(i, j);
            }else{
                if (mod <= 5 && cities[bestPath[j-10]][3] != 1){
                    swapPath(j, j-10);
                    swapPath(i, j);
                }
                else if (mod > 5 && cities[bestPath[j + 10]][3] != 1){
                    swapPath(j, j + 10);
                    swapPath(i, j);
                }
            }

        }
    }
}

void shuffle(int ary[], int size)
{
    for (int i = 0; i < size; i++)
    {
        int j = rand() % size;
        int t = ary[i];
        ary[i] = ary[j];
        ary[j] = t;
    }
}
double calcShortDistance(int start, int end){
    double distance = 0;
    double x1, x2, y1, y2;

    for (int i = start; i < end; i++)
    {
        x1 = cities[bestPath[i]][1], y1 = cities[bestPath[i]][2];
        x2 = cities[bestPath[i + 1]][1], y2 = cities[bestPath[i + 1]][2];
        if (i % 10 == 9 && cities[bestPath[i]][3] != 1)
        {
            distance += pow((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1), 0.5) * 1.1;
        }
        else
        {
            distance += pow((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1), 0.5);
        }
    }
    return distance;
}

void randomOptimizer(int range)
{
    int halfRange = range/2;
    int randomArray[range];
    int initPath[range];
    int randA, randB;
    double score, preScore, initScore;
    int getBetter;
    int progressJ = 0;
    for (int i = 1; i < 197769 - range; i+=halfRange){
        getBetter = 0;
        initScore = calcShortDistance(i-1, i+range+1);
        //初期状態
        for(int j = 0; j < range; j++){
            initPath[j] = bestPath[i + j];
            randomArray[j] = bestPath[i + j];
        }
        shuffle(randomArray, range);
        for (int j = 0; j < range; j++)
        {
            bestPath[i + j] = randomArray[j];
        }
        //最適化
        for(int j = 0; j < 3000; j++){
            preScore = calcShortDistance(i - 1, i + range + 1);
            randA = i + rand() % range;
            randB = randA;
            while(randB == randA){
                randB = i + rand() % range;
            }
            swapPath(randA, randB);
            score = calcShortDistance(i - 1, i + range + 1);
            if(score < preScore){
                j = 0;
            }else{
                swapPath(randA, randB);
            }
            if(score < initScore){
                bestScore = calcDistance();
                printf("good score %.5lf\n", bestScore);
                getBetter = 1;
                break;
            }
        }
        //良くならなかった場合
        if(getBetter == 1){
            printf("good\n good\n good\n");
        }else{
            for (int j = 0; j < range; j++)
            {
                bestPath[i + j] = initPath[j];
            }
        }
    }
    printf("round done");
}

void randomDistOptimizer()
{
    int initPath[197770];
    int randA, randB;
    double score, preScore, initScore;
    int getBetter;
    float base_x, base_y;
    int nearNum[4] = { 0 };
    float nearDist[4] = { 0 };
    int number = 4;
    float dis;
    int countImp = 0;

    for (int i = 1; i < 197769; i++){
        if(cities[bestPath[i]][3] == 1){
            printf("point %d\n\n", i);
            for(int j = 0; j < 197770; j++){
                initPath[j] = bestPath[j];
            }
            for(int j = 0; j < number; j++){
                nearNum[j] = 0;
                nearDist[j] = 10000;
            }
            getBetter = 0;
            initScore = calcDistance();
            base_x = cities[bestPath[i]][1];
            base_y = cities[bestPath[i]][2];

            for (int j = 1; j < 197770; j++){
                if(i != j){
                    dis = pow((base_x - cities[bestPath[j]][1]) * (base_x - cities[bestPath[j]][1]) + (base_y - cities[bestPath[j]][2]) * (base_y - cities[bestPath[j]][2]), 0.5);
                    for(int k=0; k< number;k++){
                        if(dis < nearDist[k]){
                            for(int l = 0; l < number-1-k; l++){
                                nearNum[number-1-l] = nearNum[number-2-l];
                                nearDist[number-1-l] = nearDist[number-2-l];
                            }
                            nearNum[k] = j;
                            nearDist[k] = dis;
                            break;
                        }
                    }
                }
            }
            // printf("%d  %d  %d\n", nearNum[0], nearNum[1], nearNum[2]);
            // printf("%f  %f  %f\n", nearDist[0], nearDist[1], nearDist[2]);
            for(int j = 0; j < 30; j++){
                for(int k = 0; k < 9; k++){
                    randA = rand() % (number+1);
                    randB = randA;
                    while(randB == randA){
                        randB = rand() % number;
                    }
                    if(randA == number){
                        swapPath(i, nearNum[randB]);
                    }else{
                        swapPath(nearNum[randA], nearNum[randB]);
                    }
                }
                score = calcDistance();
                // printf("increase %f \n", initScore - score);
                // printf("init score: %f\n", initScore);
                // printf("new  score: %f\n", score);
                if(score < initScore){
                    countImp++;
                    bestScore = calcDistance();
                    initScore = bestScore;
                    printf("good score %.5lf\n", bestScore);
                    getBetter = 1;
                    break;
                }else{
                    for(int k = 0; k < 197770; k++){
                        bestPath[k] = initPath[k];
                    }
                }
            }
            printf("count: %d\n", countImp);
            printf("best score %.5lf\n", bestScore);
            if(getBetter == 1){
                printf("good\n good\n good\n");
            }
        }
    }
    printf("round done");
}

void outputCSV(){
    FILE *fp;
    char *fname = "submission.csv";
    int ret;

    fp = fopen(fname, "w");
    if (fp == NULL)
    {
        printf("%sファイルが開けません\n", fname);
    }
    fprintf(fp, "Path\n");
    for(int i=0; i<sizeof(bestPath)/sizeof(bestPath[0]);i++){
        fprintf(fp, "%d\n", bestPath[i]);
    }

    fclose(fp);
}