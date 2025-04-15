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

const int MAX_MEHVAR = 10'000'000;
map<pll, pll> duration[MAX_MEHVAR];
vector<pll> normal;

vector<int> Read(ifstream &inp) {
    vector<int> res;
    bool isDigit = false;
    string line;
    while(sz(line) < 3)
        getline(inp, line);
    for(auto u: line) {
        if('0' <= u and u <= '9') {
            if(!isDigit) {
                res.push_back(0);
                isDigit = true;
            }
            res.back() *= 10;
            res.back() += u-'0';
        } else isDigit = false;
    }
    return res;
}

double tourism(ll count_in, ll hours_in, ll count_out, ll hours_out) {
    return (double) (hours_out*count_in - hours_in*count_out) / (count_in * count_out);
}

int main(int arc, char** argv) {
    ios_base::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
    date a = {1395, 1, 1};
    while (a.ID() != "14040101"){
        day[stoi(a.ID())] = a;
        days.push_back(a);
        a.tomorrow();
    };
    
    string s;
    cin >> s;
    assert(s == "MEHVAR,START,END,COUNT,HOURS");
    while(cin >> s) {
        if(s == "") break;
        ll mehvar = 0, start = 0, end = 0, count = 0, hours = 0;
        int p = 0;
        while(s[p] != ',') mehvar = mehvar*10+(s[p++]-'0');
        while(s[++p] != ',') start = start*10+(s[p]-'0');
        while(s[++p] != ',') end = end*10+(s[p]-'0');
        while(s[++p] != ',') count = count*10+(s[p]-'0');
        while(++p < sz(s)) hours = hours*10+(s[p]-'0');
        duration[mehvar][{start, end}] = {count, hours};
        normal.push_back({start, end});
    }
    sort(normal.begin(), normal.end());
    normal.resize(unique(normal.begin(), normal.end()) - normal.begin());
    cout << fixed << setprecision(2);
    cout << "SHAHR,START,END,TURISM" << '\n';
    ifstream ioc(argv[1]); // Input/Output of Cities
    string shahr;
    while (ioc >> shahr) {
        shahr.pop_back();
        vector<int> in = Read(ioc);
        vector<int> out = Read(ioc);
        getline(ioc, s);
        for(auto [st, en]: normal) {
            ll count_in = 0, hours_in = 0, count_out = 0, hours_out = 0;
            for(int mehvarIn: in)
                if(duration[mehvarIn].find({st, en}) != duration[mehvarIn].end()) {
                    count_in += duration[mehvarIn][{st, en}].first;
                    hours_in += duration[mehvarIn][{st, en}].second;
                }
            for(int mahvarOut: out)
                if(duration[mahvarOut].find({st, en}) != duration[mahvarOut].end()) {
                    count_out += duration[mahvarOut][{st, en}].first;
                    hours_out += duration[mahvarOut][{st, en}].second;
                }
            if(count_in == 0 || count_out == 0 || hours_in == 0 || hours_out == 0) continue;
            cout << shahr << ',' << st << ',' << en << ',' << tourism(count_in, hours_in, count_out, hours_out)*7/(day[en].order-day[st].order) << '\n';
        }
    }
    
    return 0;
}
