class Solution:
    """
    Args:
        nums: List[int]
        k: int
    Returns: List[int]
    Description: Given an array of integers nums that are nonnegative, and an integer k, return the maximum subarray whose sum is less than or equal to k.
    
    """


    def maxSubArray(self, nums, k: int) -> int:
        cur = 0
        left = -1
        arr = []

        for right in range(0,len(nums)):

            cur += nums[right]
            arr.append(nums[right])

            while cur > k:
                left += 1
                cur -= nums[left]
                arr.pop(0)

        return arr


k = 15
a = [4,5,2,0,1,8,12,3,6,9]

main = Solution()
print(main.maxSubArray(a,k))