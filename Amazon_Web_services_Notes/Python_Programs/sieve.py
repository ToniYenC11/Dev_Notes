import subprocess

def sieve(n):
    subprocess.run(['touch','results.txt']) # Creates a results.txt file
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0], is_prime[1] = False, False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    
    prime_list = [i for i, prime in enumerate(is_prime) if prime]
    
    with open('results.txt','w') as file:
        for prime in prime_list:
            file.write(f'{prime}\n')


sieve(250)
