#include <iostream>
#include <vector>
using namespace std;

vector<string> headers;

inline vector<string> split(const string &s) {
    vector<string> a = {""};
    for(auto u: s)
        if(u == ',') a.push_back("");
        else a.back() += u;
    return a;
}

int index(string s) {
    for(int i = 0; i < (int) headers.size(); i++)
        if(headers[i] == s)
            return i;
    return -1;
}

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    string s;
    cin >> s;
    headers = split(s);
    int iWD = index("WD"), iID = index("ID");
    cout << "WORK,ID,ALL\n";
    int iC[5];
    for(int i = 0; i < 5; i++)
        iC[i] = index("C"+to_string(i+1));
    int z[5] = {2, 3, 1, 30, 2};
    while(cin >> s) {
        if(s == "") break;
        vector<string> a = split(s);
        int all = 0;
        for(int i = 0; i < 5; i++) {
            if(a[iC[i]].empty())
                a[iWD] = '0';
            else
                all += (int)(stod(a[iC[i]])+0.1)*z[i];
        }
        cout << a[iWD] << ',' << a[iID] << ',' << all << '\n';
    }
    return 0;
}