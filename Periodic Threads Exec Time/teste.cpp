#include<signal.h>
#include<stdio.h>
#include<unistd.h>
#include<errno.h>
#include<sys/time.h>
#include<iostream>
#include<string>
#include<string.h>


long load=1;
void deadline();
void do_work();



void wakeup(int j){
	struct itimerval aux;
	int t1, t2;
	
	getitimer( ITIMER_REAL, &aux); 	//Get initial resume time
	
	t1 = aux.it_value.tv_usec;
	//std::cout << "Hello World! Thread working |Resume Time : " <<t1<< std::endl;
	
	do_work();
	
	getitimer( ITIMER_REAL, &aux);
	t2 = aux.it_value.tv_usec; //Get Final resume time
	
	std::cout << "Execution time (usec): " <<t1 - t2<< std::endl;
	
	if (t2==0){
		deadline();
	}
	return;
}

void do_work(){
	
	for ( int i = 0; i < load * 1000; i++) {
		/* do nothing , keep counting */
	}

}

void deadline() {
	std::cout << "Lost deadline!" <<  std::endl;
}

int main (int argc, char ** argv) {
	int i;
	int period;
	int priority;
	char scheduler[5];
	
	period = atoi(argv[1])*1000;
	priority = atoi(argv[2]);
	load = atoi(argv[3]);
	strcpy(scheduler, argv[4]);
	
	std::cout <<  " period : " << period <<"\n priority : "<< priority << "\n load : "<< load << "\n scheduler : " << scheduler <<std::endl;
	
	struct sched_param param;	//Parâmetros de escalonamento
	param.sched_priority = priority;
	
	if (scheduler[0]=='F'){
		int r = sched_setscheduler (0, SCHED_FIFO , &param);
		if(r==-1){ perror("scheduller"); return 1;}
		std::cout <<"Escalonamento FIFO: "<<r<<std::endl;
		
	}else{
		int r = sched_setscheduler (0, SCHED_RR , &param);
		if(r==-1){ perror("scheduller"); return 1;}
		std::cout <<"Escalonamento RR: "<<r<<std::endl;
	}
	
	struct itimerval val;
	struct sigaction action;
	sigset_t mask;
	
	sigemptyset(&action.sa_mask);
	action.sa_handler = wakeup;
	action.sa_flags=SA_RESTART; 
	
	if(sigaction(SIGALRM, &action, 0)==-1){
		perror("sigaction");
		return 1;
	}
	
	
	val.it_interval.tv_sec=0;
	val.it_interval.tv_usec=period;
	val.it_value.tv_sec=0;
	val.it_value.tv_usec=period;
	
	if(setitimer(ITIMER_REAL, &val, 0)==-1){
		perror("setitimer");
		return 1;
	}
	
	if(sigwait( &mask, &i)==-1){
		perror("sigwait");
	}
	
	
	return 0;

}


/*
USEFULL MATERIALS
https://www.youtube.com/watch?v=PzrOipMUV1E
*/
