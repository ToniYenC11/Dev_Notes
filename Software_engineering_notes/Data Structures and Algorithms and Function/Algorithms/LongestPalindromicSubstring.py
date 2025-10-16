class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 1:
            return ""
        
        start, length = 0, 0
        for i in range(len(s)):
            # Odd-length palindrome
            l1, len1 = self.expand(s, i, i)
            # Even-length palindrome
            l2, len2 = self.expand(s, i, i + 1)

            if len1 > length:
                start, length = l1, len1
            if len2 > length:
                start, length = l2, len2
        
        return s[start:start+length]
    
    def expand(self,s,l,r):
        start,length = l,0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            start = l
            length = r - l + 1
            l -= 1
            r += 1 
        return start, length

solution = Solution()
print(solution.longestPalindrome('cbbd'))
