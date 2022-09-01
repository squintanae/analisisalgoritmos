function generarParentesis(r,b,e,n,D)
  if b=e 
    print(D[i])
  end
  print("(")
  generarParentesis(r,b,r[b*n][e],n,D)
  generarParentesis(r,r[b*n][e+1],e,n,D)
  print(")")
end


function matMulti(D)
  n = length(D)
  #m=[0 for i=2: n, j=0:n ]
  m=[0 for i=1:n, j=1:n ]
  L=2
  
  while L<n
    i=1
    while i<n-L+1
      j = i+L-1
      m[i+1,j+1]=Inf      
      k=i 
    
      while k<=j-1
        q = m[i+1,k+1] + m[k+2,j+1] + D[i]*D[k+1]*D[j+1] 
        if q<m[i+1,j+1]
          m[i+1,j+1]=q
          r[i+1,j+1]=k
        end 
        k=k+1
      end
  
      i=i+1
    end
  L=L+1
  end
  generarParentesis(r,1,n-1,n,D)
  #println(m)
end

D = [40, 20, 30, 10, 30]
matMulti(D)