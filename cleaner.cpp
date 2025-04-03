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

struct uncleaned_data {
    int worked, time, all;
    ll id;
    void show() {
        cerr << "Worked: " << worked << ", Time: " << time << ", All: " << all << ", Id: " << id << '\n';
    }
    bool operator<(const uncleaned_data &other) {
        return time < other.time;
    }
    bool operator==(const uncleaned_data &other) {
        return id == other.id;
    }
};

ll init_z = 10LL;
inline ll completeTime(const ll a) {
    ll x = a, z = init_z;
    while(x >= 10) x /= 10, z *= 10;
    return (x >= 5 and init_z == 10? z*139 + a: z*140 + a);
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

const int MAX_MEHVAR_CODE = 10'000'000;
vector<string> headers;
vector<uncleaned_data> mehvar[MAX_MEHVAR_CODE]; 
vector<ll> hourSum;

inline bool natural(ll x, ll zx, ll y, ll zy) {
    return x*zy <= y*zx*2 && y*zx <= x*zy*2;
}

inline bool natural(int mehvarIndex, int index, int cmpIndex) {
    return natural(mehvar[mehvarIndex][index].all, hourSum[mehvar[mehvarIndex][index].time%100],
         mehvar[mehvarIndex][cmpIndex].all, hourSum[mehvar[mehvarIndex][cmpIndex].time%100]);
}

inline int predict(int mehvarIndex, int index, int beforeIndex, int afterIndex) {
    auto &before = mehvar[mehvarIndex][beforeIndex];
    auto &current = mehvar[mehvarIndex][index];
    auto &after = mehvar[mehvarIndex][afterIndex];
    return (hourSum[after.time%100]*before.all+hourSum[before.time%100]*after.all)/hourSum[after.time%100]*hourSum[current.time%100]/hourSum[before.time%100]/2;
}

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    string s;
    cin >> s;
    constexpr int iWORK = 0, iID = 1, iALL = 2;
    assert(s == "WORK,ID,ALL");
    cout << "ID,ALL\n";
    while(cin >> s) {
        if(s == "") break;
        vector<ll> a = split(s);
        if(a[iID] == 80100113202 or a[iID] == 1080100113202 or a[iID] == 120100113201 or a[iID] == 40100113201 or a[iID] == 100100113201 or a[iID] == 60100113201) {
            switch (a[iID]) {
                case 80100113202:
                    init_z *= 100LL;
                    break;
                case 1080100113202:
                    init_z /= 100LL;
                    break;
                case 120100113201:
                    init_z /= 10LL;
                    break;
                case 40100113201:
                    init_z *= 10LL;
                    break;
                case 100100113201:
                    init_z /= 10LL;
                    break;
                case 60100113201:
                    init_z *= 10LL;
                    break;
            }
        }
        auto [time, mehvar_code] = splitCompleteTimeMehvar(completeTime(a[iID]));
        if(time%100 >= 24 or time / 100 % 100 > 31 or time / 10000 % 100 > 12 or mehvar_code >= MAX_MEHVAR_CODE) {
            uncleaned_data _ = {(int) a[iWORK], time, (int) a[iALL], a[iID]};
            _.show();
        } else
            mehvar[mehvar_code].push_back({(int) a[iWORK], time, (int) a[iALL], a[iID]});
    }
    cerr << endl;
    for(int i = 0; i < MAX_MEHVAR_CODE; i++)
        if(mehvar[i].size() > 10000u) {
            sort(mehvar[i].begin(), mehvar[i].end());
            mehvar[i].resize(unique(mehvar[i].begin(), mehvar[i].end())-mehvar[i].begin());
            int len = (int) mehvar[i].size();
            bool valid[len] = {};
            hourSum.assign(24, 0);
            for(auto &u: mehvar[i])
                hourSum[u.time%100] += u.all;
            for(int j = 0; j < len; j++) {
                if(mehvar[i][j].all == 0)
                    mehvar[i][j].worked = 0;
                valid[j] = mehvar[i][j].worked == 60;
            }
            for(int j = 1; j+1 < len; j++)
                valid[j] &= natural(i, j, j-1) and natural(i, j, j+1);
            valid[0] &= natural(i, 0, 1);
            valid[len-1] &= natural(i, len-1, len-2);
            int complete_valid = 0, strange = 0, almost_complete = 0, deleted = 0;
            for(int j = 0; j < len; j++) {
                if(mehvar[i][j].worked < 60) {
                    if(mehvar[i][j].worked >= 30)
                        mehvar[i][j].all = mehvar[i][j].all*60/mehvar[i][j].worked, almost_complete++;
                    else {
                        int before = j-1, after = j+1;
                        while(before >= 0 and !valid[before]) before--;
                        while(after < len and !valid[after]) after++;
                        if(before == -1) before = after;
                        if(after == len) after = before;
                        mehvar[i][j].all = predict(i, j, before, after);
                        deleted++;
                    }
                } else if(!valid[j])
                    strange++;
                else
                    complete_valid++;
            }
            cerr << i << ' ' << complete_valid << ' ' << strange << ' ' << almost_complete << ' ' << deleted << '\n';
            for(auto &u: mehvar[i])
                cout << u.id << ',' << u.all << '\n';
        }
    return 0;
}