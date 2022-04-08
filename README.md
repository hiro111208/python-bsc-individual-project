# 6CCS3PRJ
Individual project of BSc Computer Science at King's College London

In order to execute the system, users must have a Python3 environment in their computer and be in the software directory on command line. If users wish to obtain different data, they must be familiar with the basic operations of the Python language, especially the use of for loops.

## Executing the Generation of Data
In order to obtain the data of the ratio between social utilities of a Nash equilibrium and the optimal solution, only the file "main.py" must be executed. The following are the commands users must execute to obtain the data. If users' environment already contains "openpyxl", the first command does not have to be executed. It usually takes some time to generate data.  
- pip3 install openpyxl  
- python3 main.py

## Testing
In order to conduct testing, users must execute the following command. With this command, all test files are executed.  
- python3 -m unittest discover tests

## Change Parameters
If users wish to obtain data of the ratio with different parameter settings, it can be achieved with the following way. The figures \ref{par1} and \ref{par2}  are a segment of code (from line 160 to 163 of main.py) that handle the parameter settings.

\begin{figure}[!htb]
  \noindent
  \makebox[\textwidth]{\includegraphics[scale=0.6]{Appendices/Screenshot 2022-04-08 at 11.07.30.png}}%
  \caption{Parameter setting}
  \label{par1}
\end{figure}

\begin{figure}[!htb]
  \noindent
  \makebox[\textwidth]{\includegraphics[scale=0.6]{Appendices/Screenshot 2022-04-08 at 11.15.40.png}}%
  \caption{Another parameter setting}
  \label{par2}
\end{figure}
The line 160 manipulates the parameters of player and resource, the line 161 manipulates the parameters of player's benefit and resource failure probability, the line 162 manipulates the parameters of resource cost and failure probability and the line 163 manipulates the parameters of player's benefit and resource cost.  

Users can also change how player's benefit, resource cost and failure probability change by modifying the code from line 108 to 118 in main.py.
\begin{figure}[!htb]
  \noindent
  \makebox[\textwidth]{\includegraphics[scale=0.6]{Appendices/Screenshot 2022-04-08 at 12.43.20.png}}%
  \caption{Change the functions of parameters}
  \label{change}
\end{figure}
