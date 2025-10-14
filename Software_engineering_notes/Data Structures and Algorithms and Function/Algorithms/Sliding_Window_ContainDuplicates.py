class Solution:
    def containsNearbyDuplicate(self, nums, k: int) -> bool:
        lp, rp = 0,1

        while rp < len(nums):
            while lp != rp and abs(lp - rp) > k:
                lp += 1
            left, right = nums[lp], nums[rp]
            if left == right:
                if abs(lp - rp) <= k:
                    return True
                else:
                    lp += 1
            else:
                rp += 1
        
        
        return False

# Example usage:
solution = Solution()
given = [1,0,1,1]
k = 1
print(solution.containsNearbyDuplicate(given, k))  # Output: True