#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

inline vector<ll> split(const string &s) {
    vector<ll> a = {0};
    for(auto u: s)
        if(u == ',') a.push_back(0);
        else a.back() = a.back()*10+(u-'0');
    return a;
}

inline pair<int, int> splitCompleteTimeMehvar(ll a) {
    int mehvar = 0, z = 1;
    while (a > 10'000'000'000) {
        mehvar += z * static_cast<int>(a % 10);
        a /= 10;
        z *= 10;
    }
    return {a, mehvar};
}

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    string s;
    cin >> s;
    constexpr int iID = 0, iALL = 1;
    assert(s == "ID,ALL");
    cout << "DID,ALL\n";
    int lastTime = 0, sum = 0;
    while(cin >> s) {
        if(s == "") break;
        vector<ll> a = split(s);
        auto [time, mehvar_code] = splitCompleteTimeMehvar(a[iID]);
        if(time%100 == 0)
            sum = a[iALL];
        else if(time == lastTime+1) {
            sum += a[iALL];
            if(time%100 == 23)
                cout << mehvar_code << time/100 << ',' << sum << '\n';
        }
        lastTime = time;
    }
   
    return 0;
}