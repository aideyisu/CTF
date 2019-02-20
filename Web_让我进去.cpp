#include<bits/stdc++.h>
 
 
using namespace std;
typedef unsigned int uint;
typedef long long LL;
const int MAXN = 1e6 + 5;
const int mod = 1e9 + 7;
 
struct MD5 {
 
    typedef void (MD5::*deal_fun)(uint&, uint, uint, uint, uint, uint, uint);//���ڶ��庯��ָ������
    string init_str;//�����ַ���
    uint init_arr[1000];//���յ���������{�������䴦��������}
 
 
    const static int MAXN = 1e2;
 
    static uint s_state[4];//�ʼ��Ĭ�Ͼ�̬�������
 
    uint state[4];//���Ҳ��Ĭ�Ͻ�����������ǻ�ı�
 
    static uint rolarray[4][4];//λ������
    static uint mN[4][16];//��M����Ĵ���
 
    uint curM;//��ǰ�����ֱ�������������е�λ��
    uint lenZ;//���ݵ��ܳ�{�������䴦���������ܳ����������64�ı���}
    uint offset;//��Ҫ�ӵڼ��鿪ʼ����
    uint Tarr[64];//��ǰ�����T��������
    uint Memory[64 + 5];//��ǰҪ�����64���ֽ�����
    uint M[16];//��64���ֽ����ݷ�Ϊ16����
 
    MD5();
    MD5(string str, int noffset);
 
    //���ݴ�����
    inline uint F(uint X, uint Y, uint Z);
    inline uint G(uint X, uint Y, uint Z);
    inline uint H(uint X, uint Y, uint Z);
    inline uint I(uint X, uint Y, uint Z);
 
    //ѭ�����ƺ���
    uint ROL(uint s, uint ws);
 
    //���̴�����
    inline void FF(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void GG(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void HH(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
    inline void II(uint &a, uint b, uint c, uint d, uint x, uint s, uint ac);
 
    //����T���鵥�����ݵĺ���
    inline uint T(uint i);
 
    //���������е�64���ֽ��Ƶ�Memory������
    void data_Init();
 
    //����M����
    void create_M_arr();
 
    //�ƶ�a,b,c,d��������ǰ�������
    void l_data_change(uint *buf);
 
    //����T����
    void create_T_arr();
 
    //�õ�����MD5ֵ
    string get_MD5();
 
    //���̴���
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
��ͳ�������
0x67452301,
0xefcdab89,
0x98badcfe,
0x10325476
���ĸ������ǿ��Ը���Ҫ����ĵģ����ȡ������������;����õ�MD5����Ľ����һ����
���ˣ�������Щ�����Ǿ�̬�ģ��ı�֮�󲻻������Ҫ���½��и���
*/
 
uint MD5::s_state[4] = {
    0xb2801557,
    0x06f3656c,
    0x644f6d37,
    0xc7b53ce5
};//�Ѿ���С�˹��򷴴����ϣֵ��
 
 
MD5::MD5() {}
 
MD5::MD5(string str, int noffset = 1) {
    offset = noffset;
    curM = (noffset - 1) * 64;//��0λ�ô���ʼ����
    init_str = str;//�������ַ������д���
    lenZ = init_str.length();
    memset(init_arr, 0, sizeof(init_arr));
 
    for(int i = 0; i < lenZ; i ++) {
        init_arr[i] = str[i];//���յ�����������и�ֵ
    }
    /*
        ���������䵽ȡģ64���ֽڵ���56���ֽ�
        ��һ�����0x80��Ȼ�����0x00��
    */
    if(lenZ % 64 != 56) init_arr[lenZ ++] = 0x80;
    while(lenZ % 64 != 56) {
        init_arr[lenZ ++] = 0x00;
    }
 
    /*
        ���8���ֽڱ�����û����Ǯλ���Ķ��٣���ס��λ���ĸ��������ֽڵĸ�����ͬʱ�ǰ���С�˹���
    */
    uint lengthbits = init_str.length() * 8;
    init_arr[lenZ ++] = lengthbits & 0xff;
    init_arr[lenZ ++] = lengthbits >> 8 & 0xff;
    init_arr[lenZ ++] = lengthbits >> 16 & 0xff;
    init_arr[lenZ ++] = lengthbits >> 24 & 0xff;
 
    //��Ϊuint���32λ��������ֻҪ�����ĸ��ֽھͿ����ˣ���Ȼʵ����Ҫ����64λ����
    lenZ += 4;//�ⲽ��û����������
 
 
    for(int i = 0;i < 4;i ++){
        state[i] = s_state[i];//���ʼ��Ĭ�Ͼ�̬���������ֵ����̬�������
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
 
//����ǰ�潲��
inline uint MD5::T(uint i) {
    return (uint)((0xffffffff + 1LL) * abs(sin(i)));
}
 
//ȡ64���ֽڷ���Memory������
void MD5::data_Init() {
    uint tmp = 0;
    for(int i = 0; i < 64; i ++) {
        Memory[i] = init_arr[curM + i];
    }
    curM += 64;//�仯λ��
}
 
 
void MD5::create_T_arr() {
    for(int i = 1; i <= 64; i ++) {
        Tarr[i - 1] = T(i);
    }
}
 
/*
����ʹ����С�˽����ݴ���M�����У�������΢˼��һ��
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
 
//�ƶ�a,b,c,d�����һ���Ƶ���һ��
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
        ����Ĵ���ֻ��Ϊ�˸������ѭ��
    */
    uint * a = &statetmp[0];
    uint * b = &statetmp[1];
    uint * c = &statetmp[2];
    uint * d = &statetmp[3];
 
    /*
        ����M�����T����
    */
    create_M_arr();
    create_T_arr();
 
    /*
        ��������ָ������
        ѭ������
    */
 
    deal_fun d_fun[4] = {
        &MD5::FF, &MD5::GG, &MD5::HH, &MD5::II
    };
 
    for(int i = 0; i < 4; i ++) {
        for(int j = 0; j < 16; j ++) {
            (this ->* d_fun[i])(*a, *b, *c, *d, M[mN[i][j]], rolarray[i][j % 4], Tarr[i * 16 + j]);
            l_data_change(statetmp);//����a,b,c,d
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
        ������ʾҲ����С��
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
