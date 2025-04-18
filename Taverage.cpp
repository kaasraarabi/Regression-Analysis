#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<ll, ll> pll;
#define sz(x) ((int) (x).size())

struct date {
    int year, month, day, order = -1;
    
    date() {}

    date(int _year, int _month, int _day) : year(_year), month(_month), day(_day) {
        stamp();
    }

    void tomorrow() {
        int max_day;
        if (month <= 6) {
            max_day = 31;
        } else if (month <= 11) {
            max_day = 30;
        } else {
            max_day = isKabise(year) ? 30 : 29;
        }

        if (day < max_day) {
            day++;
        } else {
            day = 1;
            if (month == 12) {
                month = 1;
                year++;
            } else {
                month++;
            }
        }
        stamp();
    }

    static bool isKabise(int y) {
        return y % 4 == 3;
    }

    void stamp() {
        int total_days = 0;
        for (int yr = 1395; yr < year; ++yr) {
            total_days += isKabise(yr) ? 366 : 365;
        }
        for (int mo = 1; mo < month; ++mo) {
            if (mo <= 6) {
                total_days += 31;
            } else if (mo <= 11) {
                total_days += 30;
            } else {
                total_days += isKabise(year) ? 30 : 29;
            }
        }
        total_days += (day - 1);
        order = total_days;
    }

    int weekday_num() const {
        return order % 7;
    }

    string weekday() const {
        const vector<string> weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
        return weekdays[weekday_num()];
    }

    bool isHoliday() const {
        int wd = weekday_num();
        vector<pair<int,int>> iranian_halidays = {
            {1, 1}, {1, 2}, {1, 3}, {1, 4}, {1, 12}, {1, 13},
            {3, 14}, {3, 15}, 
            {11, 22},
            {12, 27}, {12, 28}, {12, 29}, {12, 30}   
        };
        vector<tuple<int,int,int>> arabian_holidays = {
            {1395, 2, 2}, {1395, 2, 16}, {1395, 3, 2}, {1395, 4, 6}, {1395, 4, 16}, {1395, 4, 17}, {1395, 5, 9}, {1395, 6, 22}, {1395, 6, 30}, 
            {1395, 7, 20}, {1395, 7, 21}, {1395, 8, 30}, {1395, 9, 8}, {1395, 9, 10}, {1395, 9, 18}, {1395, 9, 27}, {1395, 12, 12},
            {1396, 1, 21}, {1396, 2, 4}, {1396, 2, 21}, {1396, 3, 25}, {1396, 4, 4}, {1396, 4, 5}, {1396, 4, 28}, {1396, 6, 18}, 
            {1396, 7, 8}, {1396, 7, 9}, {1396, 8, 18}, {1396, 8, 28}, {1396, 9, 6}, {1396, 9, 15}, {1396, 11, 30},
            {1397, 2, 10}, {1397, 3, 23}, {1397, 3, 24}, {1397, 4, 16}, {1397, 5, 29}, {1397, 6, 6}, {1397, 6, 27}, 
            {1397, 6, 28}, {1397, 8, 7}, {1397, 8, 15}, {1397, 8, 16}, {1397, 8, 24}, {1397, 9, 3}, {1397, 12, 28},
            {1398, 1, 14}, {1398, 1, 31}, {1398, 3, 4}, {1398, 3, 13}, {1398, 4, 6}, {1398, 5, 19}, {1398, 5, 27}, {1398, 6, 17},
            {1398, 6, 18}, {1398, 7, 27}, {1398, 8, 5}, {1398, 8, 6}, {1398, 8, 14}, {1398, 8, 23}, {1398, 11, 9}, {1398, 12, 18},
            {1399, 1, 20}, {1399, 2, 24}, {1399, 3, 3}, {1399, 3, 26}, {1399, 5, 8}, {1399, 5, 16}, {1399, 6, 6}, 
            {1399, 7, 16}, {1399, 7, 24}, {1399, 8, 3}, {1399, 8, 12}, {1399, 10, 28}, {1399, 12, 7}, {1399, 12, 21},
            {1400, 1, 9}, {1400, 2, 13}, {1400, 2, 22}, {1400, 2, 23}, {1400, 4, 28}, {1400, 5, 5}, {1400, 5, 25}, {1400, 5, 26}, 
            {1400, 7, 4}, {1400, 7, 12}, {1400, 7, 14}, {1400, 7, 22}, {1400, 8, 1}, {1400, 10, 16}, {1400, 11, 26}, {1400, 12, 10},
            {1401, 2, 3}, {1401, 2, 12}, {1401, 2, 13}, {1401, 3, 5}, {1401, 4, 18}, {1401, 4, 26}, {1401, 5, 15}, {1401, 5, 16}, 
            {1401, 7, 2}, {1401, 7, 4}, {1401, 7, 12}, {1401, 7, 21}, {1401, 10, 6}, {1401, 11, 16}, {1401, 11, 30}, {1401, 12, 17},
            {1402, 1, 23}, {1402, 2, 2}, {1402, 2, 25}, {1402, 4, 7}, {1402, 4, 15}, {1402, 4, 25}, {1402, 5, 4}, {1402, 5, 5},
            {1402, 6, 14}, {1402, 6, 22}, {1402, 7, 1}, {1402, 7, 10}, {1402, 9, 25}, {1402, 11, 5}, {1402, 11, 19}, {1402, 12, 6},
            {1403, 1, 22}, {1403, 1, 23}, {1403, 2, 15}, {1403, 3, 28}, {1403, 4, 5}, {1403, 4, 25}, {1403, 4, 26},
            {1403, 6, 4}, {1403, 6, 12}, {1403, 6, 14}, {1403, 6, 22}, {1403, 6, 31}, {1403, 9, 15}, {1403, 10, 25}, {1403, 11, 9}
        };
        bool isIranianHoliday = false, isArabianHoliday = false;
        for(auto [x, y]: iranian_halidays) 
            isIranianHoliday |= (x == month && y == day);
        for(auto [x, y, z]: arabian_holidays)
            isArabianHoliday |= (x == year && y == month && z == day);
        return (wd == 4 || wd == 5 || isIranianHoliday || isArabianHoliday);
    }

    string ID() {
        string res = to_string(year);
        if(month < 10) res += '0';
        res += to_string(month);
        if(day < 10) res += '0';
        res += to_string(day);
        return res;
    }
};

bool valid(const date& d) {
    if (d.year < 1395 || d.year > 1403) return false;
    if (d.month < 1 || d.month > 12) return false;

    int max_day;
    if (d.month <= 6) {
        max_day = 31;
    } else if (d.month <= 11) {
        max_day = 30;
    } else {
        max_day = date::isKabise(d.year) ? 30 : 29;
    }

    return (d.day >= 1 && d.day <= max_day);
}

const int MAX_DATE = 14040101;
date day[MAX_DATE];
vector<date> days;

inline double average(vector<double> &a) {
    return accumulate(a.begin(), a.end(), 0.0) / a.size();
}

int main(int arc, char** argv) {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    date a = {1395, 1, 1};
    while (a.ID() != "14040101"){
        day[stoi(a.ID())] = a;
        days.push_back(a);
        a.tomorrow();
    }

    string s;
    cin >> s;
    // ensure(s == "SHAHR,START,END,PRO-TOURISM")
    map<string, vector<double>> cityI;
    while(cin >> s) {
        int p = 0;
        string c = "";
        while (s[p] != ',') c += s[p++];
        while(s[++p] != ',');
        while(s[++p] != ',');
        double e = stod(s.substr(p+1));
        cityI[c].push_back(e);
    }
    vector<pair<string, vector<double>>> city(cityI.begin(), cityI.end());
    sort(city.begin(), city.end(), [](auto& a, auto& b) {
        return average(a.second) > average(b.second);
    });
    cout << fixed << setprecision(2);
    cout << "SHAHR,Average\n";
    for(auto [c, v]: city)
        cout << c << "," << average(v) << "\n";
    
    return 0;
}
