#include <stdio.h>
#include <curses.h>
#include <iostream>
#include <iomanip>
#include <omp.h>
#include <list>
#include <utility>
#include <exception>
#include <math.h>
#include <iostream>

using namespace std;

struct Result
{
	double timestamp, area;
};

double f(const double x);
const Result trapezoidalMethod(const double, const double, const double, const int);


#define TEST_CASE(x) { if (x == 0) {std::cout << __FUNCTION__ << " failed on line " << __LINE__ << std::endl;} }

void test() {
    const double dx = 0.0001;
    int accuracy = 1000;
    const short maxThreads = 10;
    short method;

    Result result = trapezoidalMethod(1.0, 4.0, dx, 10);
    TEST_CASE(round(result.area * accuracy) / accuracy == 4.714);
    cout << fixed << result.area << endl;
    std::cout << "Tests Done: " << "\n";
}

int main()
{
  std::cout << "Tests section: " << "\n";
  test(); //Test cases
	const short maxThreads = 10;
	short method;
	double x1, x2, dx;

	cout << fixed << setprecision(8) << endl;
	try
	{
		while (true)
		{
			cout << "   X1: "; cin >> x1;
			cout << "   X2: "; cin >> x2;
			cout << "   dx: "; cin >> dx;

      cout << x1 << x2 << dx;
			list<pair<short, Result>> results;
			for (int i = 0; i < maxThreads; i++)
			{
				Result result = trapezoidalMethod(x1, x2, dx, i + 1);

				pair<short, Result> s_result(i + 1, result);
				results.push_back(s_result);
			}

			cout << endl << "   Results:" << endl;
			for (auto & result : results)
			{
				cout << "   Threads: " << result.first;
				cout << ", timestamp: " << result.second.timestamp;
				cout << ", area: " << result.second.area << endl;
			}
			cout << endl;
		}
	}
	catch (exception & e)
	{
		cout << e.what() << endl;
	}
	cin.get();
	return 0;
}


const Result trapezoidalMethod(const double x1, const double x2, const double dx, const int nThreads)
{
	const int N = static_cast<int>((x2 - x1) / dx);
	double now = omp_get_wtime();
	double s = 0;

	#pragma omp parallel for num_threads(nThreads) reduction(+: s)
	for (int i = 1; i < N; i++) s += f(x1 + i * dx);

	s = (s + (f(x1) + f(x2)) / 2) * dx;

	return { omp_get_wtime() - now, s };
}

double f(const double x)
{
	return (1+x)/sqrt(2*x);
}
