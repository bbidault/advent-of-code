// https://adventofcode.com/2024/day/7

#include <cmath>
#include <fstream>
#include <sstream>
#include <vector>

/**
 * @brief Concatenate the given numbers.
 *
 * @param aNumber a number
 * @param aOtherNumber an other number
 * @return double the resulting concatenated number
 */
double concatenate( const double aNumber, const double aOtherNumber )
{
   return aNumber * pow( 10, floor( log10( aOtherNumber ) + 1 ) ) + aOtherNumber;
}

/**
 * @brief Recursive function that calculates the number of operator combinations that leads the equation to
 *        equate the given final result.
 *
 * @param aFinalResult the final result to check against
 * @param aRunningResult the result for the current recursive depth
 * @param aConstants the constants of the equation
 * @param aStep the recursive depth
 * @param aPart2 whether we are solving part 1 (addition and multiplication only) or part 2 (addition,
  *              multiplication ad concatenation)
 * @return int the number of operator combinations that leads the equation to equate the given final result.
 */
int calculate( const double           aFinalResult,
               const double           aRunningResult,
               const std::vector<int> &aConstants,
               const int              aStep,
               const bool             aPart2 )
{
   int count = 0;
   if ( aStep == aConstants.size() - 1 )
   {
      if ( aFinalResult == aRunningResult )
      {
         count++;
      }
   }
   else
   {
      // recurse for each operator
      count += calculate( aFinalResult, aRunningResult + aConstants[aStep + 1], aConstants, aStep + 1, aPart2 );
      count += calculate( aFinalResult, aRunningResult * aConstants[aStep + 1], aConstants, aStep + 1, aPart2 );
      if ( aPart2 )
      {
         count += calculate( aFinalResult, concatenate( aRunningResult, aConstants[aStep + 1] ), aConstants, aStep + 1, aPart2 );
      }
   }
   return count;
}

/**
 * @brief Sum the results of the given equations that have a valid solution, recursively try every potential
 *        operators (addition, multiplication and concatenation) to evaluate the potential solutions.
 *
 * @param aInputFilePath the input file
 * @param aPart2 whether we are solving part 1 (false) or part 2 (true)
 * @return double the sum of the results of the given equations that have a valid solution
 */
double compute( const std::string aInputFilePath, const bool aPart2 )
{
   double sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         std::stringstream ss( line );
         std::vector<std::string> equation;
         std::string numbers = "";
         while ( std::getline( ss, numbers, ':' ) )
         {
            equation.push_back( numbers );
         }

         double result = std::stod( equation[0] ); // the result of the equation

         ss = std::stringstream( equation[1] );
         std::vector<int> constants;
         while ( std::getline( ss, numbers, ' ' ) )
         {
            if ( numbers == "" )
            {
               continue;
            }
            constants.push_back( stoi( numbers ) ); // the constants of the equation
         }

         // if there is a valid solution, sum the result of the equation
         if ( calculate( result, constants[0], constants, 0, aPart2 ) > 0 )
         {
            sum += result;
         }

      }
      inputFile.close();
   }
   return sum;
}

/**
 * @brief Main function
 *
 * @param argc number of argument(s)
 * @param argv the argument(s)
 * @return int exit code
 */
int main( int argc, char *argv[] )
{
   if ( argc == 2 )
   {
      printf( "Part 1 solution: %f\n", compute( argv[1], false ) );
      printf( "Part 2 solution: %f\n", compute( argv[1], true ) );
   }

   return 0;
}
