// https://adventofcode.com/2024/day/13

#include <cmath>
#include <fstream>
#include <regex>
#include <vector>

/**
 * @brief Calculate the number of button A and B presses necessary to win the prizes (if winable).
 *
 * @param aInputFilePath the input file
 * @param aPart2 whether we are solving part 1 (false) or part 2 (true)
 * @return int64_t the sum of button A press * 3 + button B press * 1 of winable games
 */
int64_t compute( const std::string aInputFilePath, const bool aPart2 )
{
   int64_t sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<int> game;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         if ( line == "" )
         {
            double buttonAX = game[0];
            double buttonAY = game[1];
            double buttonBX = game[2];
            double buttonBY = game[3];
            double prizeX   = game[4];
            double prizeY   = game[5];
            if ( aPart2 ) // for part 2, the prize is further away
            {
               prizeX += 10000000000000;
               prizeY += 10000000000000;
            }

            // The problem can be represented by a system of two equations with two unknowns
            // prizeX = pressA * buttonAX + pressB * buttonBX
            // prizeY = pressA * buttonAY + pressB * buttonBY
            // the solution is
            double pressB = ( prizeY * buttonAX - prizeX * buttonAY ) / ( buttonBY * buttonAX - buttonBX * buttonAY );
            double pressA = ( prizeX - pressB * buttonBX ) / buttonAX;

            double intPart;// the integer part of pressA and pressB
            // verify that pressA and pressB are integers
            if ( ( modf( pressA, &intPart ) == 0 ) && ( modf( pressB, &intPart ) == 0 ) )
            {
               sum += pressA * 3 + pressB;
            }
            game.clear();
         }
         else
         {
            // parse the input
            std::regex  numReg( R"(\d+)" );
            std::smatch numMatch;
            std::string::const_iterator numSearchStart( line.cbegin() );
            while ( regex_search( numSearchStart, line.cend(), numMatch, numReg ) )
            {
               game.push_back( std::stoi( numMatch[0] ) );
               numSearchStart = numMatch.suffix().first;
            }
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
      printf( "Part 1 solution: %ld\n", compute( argv[1], false ) );
      printf( "Part 2 solution: %ld\n", compute( argv[1], true ) );
   }
   return 0;
}
