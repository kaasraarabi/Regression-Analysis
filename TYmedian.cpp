#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<ll, ll> pll;
#define sz(x) ((int) (x).size())
#define all(x) (x).begin(), (x).end()

inline double median(vector<double> &a) {
    if(!is_sorted(a.begin(), a.end()))
        sort(a.begin(), a.end());
    return a[sz(a)/2];
}

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    string s;
    cin >> s;
    // ensure(s == "SHAHR,START,END,PRO-TOURISM")
    map<string, map<int, vector<double>>> cityI;
    while(cin >> s) {
        int p = 0, en = 0;
        string c = "";
        while (s[p] != ',') c += s[p++];
        while(s[++p] != ',');
        while(s[++p] != ',')en = 10*en+(s[p]-'0');
        double e = stod(s.substr(p+1));
        cityI[c][en/10000].push_back(e);
    }
    vector<pair<string, vector<double>>> city;
    for(auto [c, d]: cityI) {
        vector<double> m(9);
        for(auto [k, v]: d)
            m[k-1398] = median(v);
        city.push_back({c, m});
    }
    sort(city.begin(), city.end(), [](pair<string, vector<double>>& a, pair<string, vector<double>>& b) {
        return *min_element(all(a.second)) > *min_element(all(b.second));
    });
    cout << fixed << setprecision(2);
    cout << "SHAHR,Median1398,Median1399,Median1400,Median1401,Median1402,Median1403\n";
    for(auto [c, v]: city) {
        cout << c;
        for(int i = 0; i < sz(v); i++)
            cout << "," << v[i];
        cout << '\n';
    }
    return 0;
}
