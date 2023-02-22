#include <iostream>
#include <unordered_map>
#include <vector>

std::pair<int, int> twoSum(std::vector<int> &nums, int target)
{
    auto hashmap = std::unordered_map<int, int>();
    for (int i = 0; i < nums.size(); ++i)
    {
        auto it = hashmap.find(target - nums[i]);
        if (it != hashmap.end())
            return std::make_pair(it->second, i);
        hashmap[nums[i]] = i;
    }
    return std::make_pair(-1, -1);
}

int main()
{
    int N, target;
    std::cin >> N >> target;
    auto arr = std::vector<int>(N);
    for (auto &elem : arr)
        std::cin >> elem;
    auto result = twoSum(arr, target);
    std::cout << result.first << " " << result.second << std::endl;
}