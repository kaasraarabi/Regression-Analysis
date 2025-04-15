#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
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

const int MAX_DATE = 14040101;
date day[MAX_DATE];
vector<date> days;
vector<date> normal;

const int MAX_MEHVAR = 10'000'000;

struct record {
    int date, hour, all;
    int stamp() {
        return 24*day[date].order + hour;
    }
};
vector<record> mehvar[MAX_MEHVAR];


int main() {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    date a = {1395, 1, 1};
    while (a.ID() != "14040101"){
        day[stoi(a.ID())] = a;
        days.push_back(a);
        a.tomorrow();
    };
    
    normal.push_back(days[0]);;
    for(int i = 2; i < sz(days); i++)
        if(days[i].weekday() == "Monday") {
            bool isNearHoliday = false;
            for(int j = i-2; j <= i+2; j++)
                isNearHoliday |= days[j].isHoliday();
            if(!isNearHoliday)
                normal.push_back(days[i]);
        }
    
    string s;
    cin >> s;
    assert(s == "ID,ALL");
    while(cin >> s) {
        if(s == "") break;
        record d = {0,0,0};
        int p = 0;
        while(p < 8)
            d.date = d.date * 10 + (s[p++] - '0');
        while(p < 10)
            d.hour = d.hour * 10 + (s[p++] - '0');
        int mehvarID = 0;
        while(s[p] != ',')
            mehvarID = mehvarID * 10 + (s[p++] - '0');
        while (++p < sz(s))
            d.all = d.all * 10 + (s[p] - '0');
        mehvar[mehvarID].push_back(d);
    }
    cout << "MEHVAR,START,END,COUNT,HOURS" << '\n';
    for(int i = 0; i < MAX_MEHVAR; i++)
        if(!mehvar[i].empty()) {
            int rnorm = 0;
            int pl = 0, pr = 0;
            while (++rnorm < sz(normal)) {
                while(pl < sz(mehvar[i]) && day[mehvar[i][pl].date].order < normal[rnorm-1].order) pl++;
                while(pr < sz(mehvar[i]) && day[mehvar[i][pr].date].order < normal[rnorm].order) pr++;
                if(day[mehvar[i][pl].date].order == normal[rnorm-1].order && 
                    day[mehvar[i][pr].date].order == normal[rnorm].order) {
                        unsigned int count = 0, hours = 0;
                        for(int j = pl; j < pr; j++)
                            count += mehvar[i][j].all, hours += mehvar[i][j].all*(mehvar[i][j].stamp() - mehvar[i][pl].stamp());
                        cout << i << ',' << normal[rnorm-1].ID() << ',' << normal[rnorm].ID() << ',' << count << ',' << hours << '\n';
                    }
            }
        }
    

    return 0;
}
