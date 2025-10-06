class Solution:
    
    """
    Args:
        nums: List[int]
        k: int
    Returns: List[int]
    Description: Given an array of integers nums, find the array of size k that has the maximum sum. Return its sum and the array in a dictionary with "max sum" 
    as the sum value, and "sub_array" as the array value.
    
    """
    
    def maxSubArray(self, nums, k: int) -> int:
        cur = 0
        best = float('-inf')

        for i in range(0,len(nums) - k):
            cur = sum(nums[i:i+k])
            if cur > best:
                best = cur
            if cur < 0:
                cur = 0
        return {
            "max_sum": best,
            "sub_array": nums[i:i+k]
        }


k=5
a = [8,3,-2,4,5,-1,0,5,3,9,6]

main = Solution()
print(main.maxSubArray(a,k))