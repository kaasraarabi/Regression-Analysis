// In the name of Allah
#include <bits/stdc++.h>
using namespace std;
#define sz(x) ((int)(x).size())

struct City {
    string name;
    vector<string> inputs;
    vector<string> outputs;
    vector<int> codepoints;
};

unordered_map<string, vector<int>> code_point_cache;

vector<int> utf8_to_codepoints(const string &s) {
    vector<int> codepoints;
    for (int i = 0; i < sz(s);) {
        unsigned char c = s[i];
        int code = 0, len = 0;
        if (c <= 0x7F) len = 1;
        else if ((c & 0xE0) == 0xC0) len = 2;
        else if ((c & 0xF0) == 0xE0) len = 3;
        else if ((c & 0xF8) == 0xF0) len = 4;
        else { i++; continue; }

        if (i + len > sz(s)) break;
        for (int j = 0; j < len; j++) 
            code = (j ? code << 6 : code) | (s[i + j] & (j ? 0x3F : 0xFF >> (len + 1)));
        codepoints.push_back(code);
        i += len;
    }
    return codepoints;
}

vector<int> cached_codepoints(const string &s) {
    auto it = code_point_cache.find(s);
    return it != code_point_cache.end() ? it->second : (code_point_cache[s] = utf8_to_codepoints(s));
}

bool are_equal(const vector<int>& a, const vector<int>& b) {
    if (a == b) return true;
    
    // Full LCS implementation
    int m = sz(a), n = sz(b);
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (a[i-1] == b[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    
    int lcs_length = dp[m][n];
    return 5 * lcs_length > 2 * (m + n);
}

int main() {
    vector<City> cities;
    unordered_map<string, int> city_index; // name to index in cities vector

    // Read CSV data
    string line;
    getline(cin, line); // Skip header
    while (getline(cin, line)) {
        vector<string> tokens;
        for (size_t pos = 0, cnt = 0; cnt++ < 8; pos = line.find(',', pos) + 1)
            tokens.push_back(line.substr(pos, line.find(',', pos) - pos));
        
        if (sz(tokens) < 8) continue;
        
        string code = tokens[0];
        string origin = tokens[3];
        string destination = tokens[4];
        
        auto origin_cps = cached_codepoints(origin);
        auto dest_cps = cached_codepoints(destination);

        // Find or create origin city
        int origin_idx = -1;
        for (int i = 0; i < sz(cities); i++) {
            if (are_equal(cities[i].codepoints, origin_cps)) {
                origin_idx = i;
                break;
            }
        }
        if (origin_idx == -1) {
            origin_idx = sz(cities);
            cities.push_back({origin, {}, {}, origin_cps});
            city_index[origin] = origin_idx;
        }

        // Find or create destination city
        int dest_idx = -1;
        for (int i = 0; i < sz(cities); i++) {
            if (are_equal(cities[i].codepoints, dest_cps)) {
                dest_idx = i;
                break;
            }
        }
        if (dest_idx == -1) {
            dest_idx = sz(cities);
            cities.push_back({destination, {}, {}, dest_cps});
            city_index[destination] = dest_idx;
        }

        // Add to outputs of origin and inputs of destination
        cities[origin_idx].outputs.push_back(code);
        cities[dest_idx].inputs.push_back(code);
    }

    sort(cities.begin(), cities.end(), [](const City& a, const City& b) {
        return sz(a.inputs)+sz(a.outputs) > sz(b.inputs)+sz(b.outputs);
    });

    // Output results
    for (const auto& city : cities) {
        if(city.inputs.empty() || city.outputs.empty()) continue;
        cout << city.name << ":\n";
        cout << "  Inputs: ";
        for (const auto& in : city.inputs) cout << in << " ";
        cout << "\n  Outputs: ";
        for (const auto& out : city.outputs) cout << out << " ";
        cout << "\n\n";
    }

    return 0;
}