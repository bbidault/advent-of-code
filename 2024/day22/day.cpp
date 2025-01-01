// https://adventofcode.com/2024/day/22

#include <fstream>
#include <map>
#include <vector>

/**
 * @brief Calculate the new secret number given a secret number.
 *
 * @param aSecretNumber a secret number
 * @return int64_t the new secret number
 */
int64_t newSecretNumber( int64_t aSecretNumber )
{
   int64_t sn = aSecretNumber * 64;
   aSecretNumber = sn ^ aSecretNumber;
   aSecretNumber = aSecretNumber % 16777216;
   sn            = aSecretNumber >> 5;
   aSecretNumber = sn ^ aSecretNumber;
   aSecretNumber = aSecretNumber % 16777216;
   sn            = aSecretNumber * 2048;
   aSecretNumber = sn ^ aSecretNumber;
   aSecretNumber = aSecretNumber % 16777216;
   return aSecretNumber;
}

/**
 * @brief For part 1, calculate the sum of the 2000th secret number of each monkey.
 *        For part 2, calculate the max number of bananas we could win by selling out hiding places for a specific
 *                    set of four last hiding places price differences.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int64_t the sum of the 2000th secret number of each monkey or the max number of bananas we could win
 */
int64_t compute( const std::string aInputFilePath, const bool aPart1 )
{
   int64_t sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      // define a map with the last four price differences as key and whether this price difference as already been seen or not
      // and the total winnings we would make if we sold the hiding place for this set of four price differences has value
      std::map<std::tuple<int, int, int, int>, std::pair<bool, int> > bananas;

      std::string line = "";
      while ( std::getline( inputFile, line ) )          // for each monkey
      {
         std::vector<std::pair<int, int> > diffAndPrice; // vector of price differences and prices
         int64_t secretNumber = std::stoi( line );
         // calculate the first 2000 secret numbers
         for ( int i = 0; i < 2000; i++ )
         {
            int64_t nsc = newSecretNumber( secretNumber );
            // the price is the last digit of the secret number
            diffAndPrice.push_back( std::make_pair( nsc % 10 - secretNumber % 10, nsc % 10 ) );
            secretNumber = nsc;
         }
         if ( aPart1 ) // for part 1, sum the secret numbers
         {
            sum += secretNumber;
         }
         else // else, for part 2
         {
            for ( int i = 3; i < diffAndPrice.size(); i++ )
            {
               std::tuple<int, int, int, int> lastFourDiff = std::make_tuple( diffAndPrice[i - 3].first,
                                                                              diffAndPrice[i - 2].first,
                                                                              diffAndPrice[i - 1].first,
                                                                              diffAndPrice[i].first );

               // if this set of last four price differences is new for this monkey
               if ( bananas.contains( lastFourDiff ) && ( false == bananas[lastFourDiff].first ) )
               {
                  bananas[lastFourDiff].first   = true; // don't consider this set of price differences again for this monkey
                  bananas[lastFourDiff].second += diffAndPrice[i].second;
               }
               // if this set of last four price differences is new for any monkey
               else if ( false == bananas.contains( lastFourDiff ) )
               {
                  bananas[lastFourDiff] = std::make_pair( true, diffAndPrice[i].second );
               }
               else
               {
                  // do nothing
               }
            }
         }
         // reinitialize the boolean that indicates whether this set of price differences has been seen for a monkey
         // to false for the next monkey
         std::map<std::tuple<int, int, int, int>, std::pair<bool, int> >::iterator banana_itr = bananas.begin();
         for (; banana_itr != bananas.end(); banana_itr++ )
         {
            banana_itr->second.first = false;
         }
      }
      if ( false == aPart1 ) // if part 2
      {
         // get the max number of bananas we could win
         std::map<std::tuple<int, int, int, int>, std::pair<bool, int> >::iterator banana_itr = bananas.begin();
         for (; banana_itr != bananas.end(); banana_itr++ )
         {
            if ( banana_itr->second.second > sum )
            {
               sum = banana_itr->second.second;
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
      printf( "Part 1 solution: %ld\n", compute( argv[1], true ) );
      printf( "Part 2 solution: %ld\n", compute( argv[1], false ) );
   }
   return 0;
}
