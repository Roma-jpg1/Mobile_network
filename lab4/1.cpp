#include <iostream>
#include <vector>
#include <array>
#include <cmath>
using namespace std;



vector<int> generate_gold(int x, int y, int takt) {
    array<int, 5> xr={};
    array<int, 5> yr={};

    for (int i =0; i<5; i++){
        xr[i] = x>>(4-i)&1;
        yr[i] = y>>(4-i)&1;
    }

    vector<int> gold;
    for (int i=0; i<takt; i++){
        int br = xr[4] ^ yr[4];
        gold.push_back(br);

        int new_x = xr[3] ^ xr[4];
        int new_y = yr[1] ^ yr[4];

        xr = {new_x, xr[0], xr[1], xr[2], xr[3]};
        yr = {new_y, yr[0], yr[1], yr[2], yr[3]};
    }
    return gold;
}




int checkPosl(const vector<int>& bits) {
    int n = bits.size();
    int o = 0;

    for (int bit : bits) {
        o += bit;
    }

    bool checks[3];

    int z = n - o;
    checks[0] = (abs(o - z) <= 1); //нули

    vector<int> cycles(n + 1, 0);
    int total_cycles = 0;

    for (int i = 0; i < n; i++) {
        if (bits[i] == bits[(i + n - 1) % n]) continue;

        int length = 1;
        while (length < n && bits[(i + length) % n] == bits[i]) {
            length++;
        }

        cycles[length]++;
        total_cycles++;
    }

    if (total_cycles == 0) {
        cycles[n] = 1;
        total_cycles = 1;
    }

    double ex = total_cycles / 2.0;
    checks[1] = 1;   // циклы

    for (int length = 1; length <= n; length++) {
        if (abs(cycles[length] - ex) > 1.0) {
            checks[1] = 0;
        }
        ex /= 2.0;
    }

    // Автокорреляция
    checks[2] = 1;

    for (int shift = 1; shift < n; shift++) {
        int sum = 0;

        for (int i = 0; i < n; i++) {
            sum += (bits[i] == bits[(i + shift) % n]) ? 1 : -1;
        }

        if (sum != -1) {
            checks[2] = 0;
        }
    }

    cout<<"chekers"<<checks[0]<<" "<<checks[1]<<" "<<checks[2]<<endl;


    // Если все три проверки равны 1, возвращаем 1
    for (int i = 0; i < 3; i++) {
        if (checks[i] != 1) return 0;
    }


    return 1;
}


int main(){
    int x = 17;
    int y = x+7;
    int takt =31;

    vector<int> chehov = {
    1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0,
    0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0
};
   
    vector<int> result = generate_gold(x, y, takt);
    vector<int> autocor(31);

    vector<int> result2 = generate_gold(x+1, y-5, takt);

    for (int i=0; i<result.size(); i++){
        autocor[i] = result[i];
    }

    for (int i=0; i<result.size(); i++){
        cout<<result[i]<<" ";
    }
    cout<<endl;


    for (int k=0; k<=takt; k++){
        int same=0;
        int diff=0;
        for (int i=0; i<takt; i++){
            if (result[i] == autocor[i]){
                same++;
            } else {
                diff++;
            }
        }
        double R = double(same-diff)/double(takt);
        cout<<"Shift "<<k<<": R = "<<R<<endl;

        int last = autocor.back();
        autocor.pop_back();
        autocor.insert(autocor.begin(), last);
    }

    int same2 = 0;
    int diff2 = 0;

    for (int i = 0; i < takt; i++) {
        if (result[i] == result2[i]) {
            same2++;
        } else {
            diff2++;
        }
    }
    double R2 = double(same2-diff2)/double(takt);
    cout<<"4n correlation = "<<R2<<endl;


    bool check_res = checkPosl(chehov);


    cout<<"Pseudorandomness check: "<<check_res<<endl;
}