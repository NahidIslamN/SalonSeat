#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        long long p, q;
        cin >> p >> q;

        __int128 lhs = 3 * (__int128)p;
        __int128 low = 2 * (__int128)q;
        __int128 high = 3 * (__int128)q;

        if (low <= lhs && lhs < high) {
            cout << "Bob\n";
        } else {
            cout << "Alice\n";
        }
    }

    return 0;
}
