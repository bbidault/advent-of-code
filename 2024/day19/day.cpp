// https://adventofcode.com/2024/day/19

#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <vector>

/**
 * @brief Recursive function. Calculate the number of combinations of given patterns that match the given design.
 *
 * @param aDesign a design to reproduce with patterns
 * @param aPatterns a set of patterns
 * @param aCache a map of designs and number of valid pattern combinations
 * @return the number of combinations of given patterns that match the given design
 */
int64_t combinations( const std::string              aDesign,
                      const std::set<std::string>    &aPatterns,
                      std::map<std::string, int64_t> &aCache )
{
   // if the count of pattern combinations has already been calculated for the design, return it now
   if ( aCache.contains( aDesign ) )
   {
      return aCache[aDesign];
   }
   // else, calculate it
   int64_t count     = 0;
   int subDesignSize = aDesign.size(); // calculate for the larger sub design first
   while ( subDesignSize > 0 )
   {
      // if the sub design is a valid pattern
      if ( aPatterns.contains( aDesign.substr( 0, subDesignSize ) ) )
      {
         if ( aDesign.size() == subDesignSize )
         {
            // the full design is a valid pattern
            count++;
         }
         else
         {
            // recursive call for the leftover design
            count += combinations( aDesign.substr( subDesignSize ), aPatterns, aCache );
         }
      }
      subDesignSize--;
   }
   aCache[aDesign] = count; // add the design to the cache memory
   return count;
}

/**
 * @brief For part 1, calculate the number of given designs that can be reproduced with the given patterns.
 *        For part 2, calculate the sum of the number of combinations of given patterns that match the given designs.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the number of given designs that can be reproduced with the given patterns or the number of combinations
 *             of given patterns that match the given designs.
 */
int64_t compute( const std::string aInputFilePath, const bool aPart1 )
{
   int64_t count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::set<std::string> patterns;

      std::vector<std::string> designs;
      bool readPatterns = true;
      std::string line  = "";
      while ( std::getline( inputFile, line ) )
      {
         if ( line.empty() )
         {
            readPatterns = false;
         }
         else if ( readPatterns )
         {
            std::stringstream ss( line );
            std::string pattern;
            while ( std::getline( ss, pattern, ',' ) )
            {
               pattern.erase( std::remove_if( pattern.begin(), pattern.end(), isspace ), pattern.end() );
               patterns.insert( pattern );
            }
         }
         else // read designs
         {
            designs.push_back( line );
         }
      }

      std::map<std::string, int64_t> cache;
      for ( int i = 0; i < designs.size(); i++ )
      {
         if ( aPart1 )
         {
            if ( combinations( designs[i], patterns, cache ) > 0 )
            {
               count++;
            }
         }
         else
         {
            count += combinations( designs[i], patterns, cache );
         }
      }

      inputFile.close();
   }
   return count;
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
