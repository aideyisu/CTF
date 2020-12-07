#include<bits/stdc++.h>
 
 
using namespace std;
typedef unsigned int uint;
typedef long long LL;
const int MAXN = 1e6 + 5;
const int mod = 1e9 + 7;
 
struct MD5 {
 
    typedef void (MD5::*deal_fun)(uint&, uint, uint, uint, uint, uint, uint);//用于定义函数指针数组
    string init_str;//数据字符串
    uint init_arr[1000];//最终的数据数组{进行扩充处理后的数据}
 
 
    const static int MAXN = 1e2;
 
    static uint s_state[4];//最开始的默认静态渐变变量
 
    uint state[4];//这个也是默认渐变变量，但是会改变
 
    static uint rolarray[4][4];//位移数组
    static uint mN[4][16];//对M数组的处理
 
    uint curM;//当前处理的直接在整个数据中的位置
    uint lenZ;//数据的总长{进行扩充处理后的数据总长，这个数是64的倍数}
    uint offset;//需要从第几组开始处理
    uint Tarr[64];//当前保存的T数组数据
    uint Memory[64 + 5];//当前要处理的64个字节数据
    uint M[16];//将64个字节数据分为16个数
 
    MD5();
    MD5(string str, int noffset);
 
    //数据处理函数
    inline uint F(uint X, uint Y, uint Z);
    inline uint G(uint X, uint Y, uint Z);
    inline uint H(uint X, uint Y, uint Z);
    inline uint I(uint X, uint Y, uint Z);
 
    //循环左移函数
    uint ROL(uint s, uint ws);
 
    //过程处理函数
    inline void FF(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void GG(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void HH(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void II(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
 
    //生成T数组单个数据的函数
    inline uint T(uint i);
 
    //将总数据中的64个字节移到Memory数组中
    void data_Init();
 
    //建立M数组
    void create_M_arr();
 
    //移动a,b,c,d，规则在前面介绍了
    void l_data_change(uint *buf);
 
    //产生T数组
    void create_T_arr();
 
    //得到最终MD5值
    string get_MD5();
 
    //过程处理
    void processing();
 
};
 
uint MD5::rolarray[4][4] = {
    { 7, 12, 17, 22 },
    { 5, 9, 14, 20 },
    { 4, 11, 16, 23 },
    { 6, 10, 15, 21 }
};
 
uint MD5::mN[4][16] = {
    { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 },
    { 1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12 },
    { 5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2 },
    { 0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9 }
};
 
/*
传统渐变变量
0x67452301,
0xefcdab89,
0x98badcfe,
0x10325476
这四个东西是可以根据要求更改的，如果取上述几个数则和经常用的MD5算出的结果是一样的
对了，由于有些数据是静态的，改变之后不会进行需要重新进行复制
*/
 
uint MD5::s_state[4] = {
    0xb2801557,
    0x06f3656c,
    0x644f6d37,
    0xc7b53ce5
};//已经按小端规则反处理哈希值了
 
 
MD5::MD5() {}
 
MD5::MD5(string str, int noffset = 1) {
    offset = noffset;
    curM = (noffset - 1) * 64;//从0位置处开始处理
    init_str = str;//对数据字符串进行处理
    lenZ = init_str.length();
    memset(init_arr, 0, sizeof(init_arr));
 
    for(int i = 0; i < lenZ; i ++) {
        init_arr[i] = str[i];//最终的数据数组进行赋值
    }
    /*
        将数据扩充到取模64个字节等于56个字节
        第一个填充0x80，然后就是0x00了
    */
    if(lenZ % 64 != 56) init_arr[lenZ ++] = 0x80;
    while(lenZ % 64 != 56) {
        init_arr[lenZ ++] = 0x00;
    }
 
    /*
        最后8个字节保存了没扩充钱位数的多少，记住是位数的个数不是字节的个数，同时是按照小端规则
    */
    uint lengthbits = init_str.length() * 8;
    init_arr[lenZ ++] = lengthbits & 0xff;
    init_arr[lenZ ++] = lengthbits >> 8 & 0xff;
    init_arr[lenZ ++] = lengthbits >> 16 & 0xff;
    init_arr[lenZ ++] = lengthbits >> 24 & 0xff;
 
    //因为uint最多32位所以我们只要考虑四个字节就可以了，虽然实际上要考虑64位，嘿
    lenZ += 4;//这步我没读懂！！！
 
 
    for(int i = 0;i < 4;i ++){
        state[i] = s_state[i];//将最开始的默认静态渐变变量赋值给静态渐变变量
    }
 
}
 
inline uint MD5::F(uint X, uint Y, uint Z) {
    return (X & Y) | ((~X) & Z);
}
inline uint MD5::G(uint X, uint Y, uint Z) {
    return (X & Z) | (Y & (~Z));
}
inline uint MD5::H(uint X, uint Y, uint Z) {
    return X ^ Y ^ Z;
}
inline uint MD5::I(uint X, uint Y, uint Z) {
    return Y ^ (X | (~Z));
}
uint MD5::ROL(uint s, uint ws) {
    return (s << ws) | (s >> (32 - ws));
}
 
 
inline void MD5::FF(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac) {
    a = ROL(a + F(b, c, d) + x + ac, s) + b;
    //printf("ff\n");
}
 
inline void MD5::GG(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac) {
    a = ROL(a + G(b, c, d) + x + ac, s) + b;
    //printf("gg\n");
}
 
inline void MD5::HH(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac) {
    a = ROL(a + H(b, c, d) + x + ac, s) + b;
    //printf("hh\n");
}
 
inline void MD5::II(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac) {
    a = ROL(a + I(b, c, d) + x + ac, s) + b;
    //printf("ii\n");
}
 
//这里前面讲了
inline uint MD5::T(uint i) {
    return (uint)((0xffffffff + 1LL) * abs(sin(i)));
}
 
//取64个字节放在Memory数组中
void MD5::data_Init() {
    uint tmp = 0;
    for(int i = 0; i < 64; i ++) {
        Memory[i] = init_arr[curM + i];
    }
    curM += 64;//变化位置
}
 
 
void MD5::create_T_arr() {
    for(int i = 1; i <= 64; i ++) {
        Tarr[i - 1] = T(i);
    }
}
 
/*
这里使用了小端将数据存在M数组中，可以稍微思考一下
*/
void MD5::create_M_arr() {
    uint tmp = 0;
    int cnt = 0;
    for(int i = 0; i < 64; i += 4) {
        tmp = 0;
        for(int j = 3; j >= 0; j --) {
            tmp |= Memory[i + j];
            if(j == 0) break;
            tmp <<= 8;
        }
        M[cnt ++] = tmp;
    }
}
 
//移动a,b,c,d，最后一个移到第一个
void MD5::l_data_change(uint *buf) {
    uint buftmp[4] = {buf[3], buf[0], buf[1], buf[2]};
    for(int i = 0; i < 4; i ++) {
        buf[i] = buftmp[i];
    }
}
 
void MD5::processing() {
    uint statetmp[4];
    for(int i = 0; i < 4; i ++) {
        statetmp[i] = state[i];
    }
    /*
        这里的处理只是为了更方便的循环
    */
    uint * a = &statetmp[0];
    uint * b = &statetmp[1];
    uint * c = &statetmp[2];
    uint * d = &statetmp[3];
 
    /*
        产生M数组和T数组
    */
    create_M_arr();
    create_T_arr();
 
    /*
        建立函数指针数组
        循环处理
    */
 
    deal_fun d_fun[4] = {
        &MD5::FF, &MD5::GG, &MD5::HH, &MD5::II
    };
 
    for(int i = 0; i < 4; i ++) {
        for(int j = 0; j < 16; j ++) {
            (this ->* d_fun[i])(*a, *b, *c, *d, M[mN[i][j]], rolarray[i][j % 4], Tarr[i * 16 + j]);
            l_data_change(statetmp);//交换a,b,c,d
        }
    }
 
 
    for(int i = 0; i < 4; i ++) {
        state[i] += statetmp[i];
    }
}
 
string MD5::get_MD5() {
    string result;
    char tmp[15];
    for(int i = 0;i < (lenZ - (offset - 1) * 64) / 64;i ++){
        data_Init();
        processing();
    }
 
    /*
        最终显示也是用小端
    */
 
    for(int i = 0; i < 4; i ++) {
        sprintf(tmp, "%02x", state[i] & 0xff);
        result += tmp;
        sprintf(tmp, "%02x", state[i] >> 8 & 0xff);
        result += tmp;
        sprintf(tmp, "%02x", state[i] >> 16 & 0xff);
        result += tmp;
        sprintf(tmp, "%02x", state[i] >> 24 & 0xff);
        result += tmp;
    }
    return result;
}
 
int main() {
    MD5 md1("123456789123456adminadmin123456789123456789123456789123456789123admin",2);
    cout << md1.get_MD5() << endl;
    return 0;
}
