#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct Job {
    int id;
    int deadline;
    int profit;
};

// Comparison function to sort jobs by profit in descending order
bool compare(Job a, Job b) {
    return a.profit > b.profit;
}

// Function to schedule jobs to maximize profit
int jobScheduling(vector<Job>& jobs) {
    sort(jobs.begin(), jobs.end(), compare);  // Sort jobs by profit

    int maxDeadline = 0;
    for (auto job : jobs)
        maxDeadline = max(maxDeadline, job.deadline);

    vector<bool> slot(maxDeadline, false);  // Time slots
    vector<int> selectedJobs;               // To store selected job IDs
    int totalProfit = 0;

    for (auto job : jobs) {
        // Find a free slot from job.deadline-1 to 0
        for (int j = job.deadline - 1; j >= 0; j--) {
            if (!slot[j]) {
                slot[j] = true;
                selectedJobs.push_back(job.id);
                totalProfit += job.profit;
                break;
            }
        }
    }
    // Print selected job IDs
    cout << "Selected Job IDs: ";
    for (int id : selectedJobs)
        cout << id << " ";
    cout << endl;

    return totalProfit;
}

// Main function
int main() {
    int n;
    cout << "Enter number of jobs: ";
    cin >> n;

    vector<Job> jobs(n);
    cout << "Enter deadline and profit for each job:\n";
    for (int i = 0; i < n; ++i) {
        cin >> jobs[i].deadline >> jobs[i].profit;
        jobs[i].id = i + 1;  // Assign job ID
    }

    int maxProfit = jobScheduling(jobs);
    cout << "Maximum Profit: " << maxProfit << endl;

    return 0;
}

// Greedy Concept:
// Jobs are sorted in descending order of profit, and each job is scheduled as late as possible before its deadline, to maximize total profit — a greedy selection.

// Time Complexity:
//     Sorting: O(n log n)
//     Scheduling: O(n²) or O(n log n) with disjoint sets
// Space Complexity:
//     O(n) (for slot tracking)


