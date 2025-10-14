
#* Sieve of Eratosthenes - Find the prime numbers up to a specified integer.

def sieve_iteration(n,prime):
    p = 2 
    while p*p <= n:
        if prime[p]:
            for num in range(p*p, n+1, p):
                prime[num] = False
        p+= 1
    return [num for num,val in enumerate(prime) if val is True]

n= 200
prime = [True] * (n+1)
prime[0],prime[1] = False, False 

print(sieve_iteration(n))