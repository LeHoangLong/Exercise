#include <stdio.h>



int main(){
	int a = 0;
	if (!a){
		printf("%d\n", a);	
	}
	a = 1;
	if (!a){
		printf("%d\n", a);
	}
	a = -1;
		printf("%d\n", !a);
	if ((!a)){
		printf("%d\n", a);
	}

	a = -8;
		printf("%d\n", !a);
	if (!a){
		printf("%d\n", a);
	}
	return 0;
}
