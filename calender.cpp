#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct date {
    int year, month, day;

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
    }

    static bool isKabise(int y) {
        return y % 4 == 3;
    }

    int weekday_num() const {
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
        return total_days % 7;
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
        bool isIranianHoliday = false;
        for(auto [x, y]: iranian_halidays) 
            isIranianHoliday |= (x == month && y == day);
        return (wd == 4 || wd == 5 || isIranianHoliday);
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

int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    date a = {1395, 1, 1};
    while (a.ID() != "14040101"){
        cout << a.ID() << ',' << a.weekday() << ',' << a.isHoliday() << '\n';
        a.tomorrow();
    }
    
    return 0;
}
