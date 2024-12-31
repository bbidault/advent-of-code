// https://adventofcode.com/2024/day/21

#include <fstream>
#include <map>
#include <regex>
#include <vector>

// a lookup table that defines the keys to enter on the directional keypad to go from one key to the next
// on another directional keypad.
std::map<std::string, std::string> directionalKeypadLookupTable = {
   { "^^", "A"    },
   { "^A", ">A"   },
   { "^<", "v<A"  },
   { "^v", "vA"   },
   { "^>", "v>A"  },
   { "A^", "<A"   },
   { "AA", "A"    },
   { "A<", "v<<A" },
   { "Av", "<vA"  },
   { "A>", "vA"   },
   { "<^", ">^A"  },
   { "<A", ">>^A" },
   { "<<", "A"    },
   { "<v", ">A"   },
   { "<>", ">>A"  },
   { "v^", "^A"   },
   { "vA", "^>A"  },
   { "v<", "<A"   },
   { "vv", "A"    },
   { "v>", ">A"   },
   { ">^", "<^A"  },
   { ">A", "^A"   },
   { "><", "<<A"  },
   { ">v", "<A"   },
   { ">>", "A"    }
};

/**
 * @brief a Location
 */
struct Location
{
   int mX = 0;
   int mY = 0;
};

/**
 * @brief a factory method to create a Location
 *
 * @param aX the x coordinate of the Location
 * @param aY the y coordinate of the Location
 * @return Location a Location
 */
Location makeLocation( const int aX, const int aY )
{
   Location loc;
   loc.mX = aX;
   loc.mY = aY;
   return loc;
}

/**
 * @brief Determines the keys to type on a directional keypad to command a robot to type the given sequence
 *        on a numerical keypad.
 *
 * @note there are 11 keys on the numerical keypad 0-9 + A, which makes a total of 121 source to target key
 *       possibilities, using a lookup table like for the directional keypad is less feasible.
 *
 * @param aSequence a sequence of keys to type on a numerical keypad
 * @return std::string a sequence of keys on a directional keypad
 */
std::string numericKeypad( const std::string &aSequence )
{
   // define the keypad
   std::map<char, Location> keypad;
   keypad['7'] = makeLocation( 0, 0 );
   keypad['8'] = makeLocation( 0, 1 );
   keypad['9'] = makeLocation( 0, 2 );
   keypad['4'] = makeLocation( 1, 0 );
   keypad['5'] = makeLocation( 1, 1 );
   keypad['6'] = makeLocation( 1, 2 );
   keypad['1'] = makeLocation( 2, 0 );
   keypad['2'] = makeLocation( 2, 1 );
   keypad['3'] = makeLocation( 2, 2 );
   keypad['0'] = makeLocation( 3, 1 );
   keypad['A'] = makeLocation( 3, 2 );
   char current = 'A';

   std::string returnSequence = "";
   // for each source and target keys on the numerical keypad, determine the directional keypad keys that need to be typed
   for ( int i = 0; i < aSequence.size(); i++ )
   {
      Location source = keypad[current];
      Location target = keypad[aSequence[i]];
      int xDiff       = target.mX - source.mX;
      int yDiff       = target.mY - source.mY;

      if ( ( source.mX == 3 ) && ( target.mY == 0 ) )
      {
         // if we are going from the bottom row to the left column, go up first then left to avoid the empty space
         for ( int j = 0; j < -xDiff; j++ )
         {
            returnSequence.push_back( '^' );
         }
         for ( int j = 0; j < -yDiff; j++ )
         {
            returnSequence.push_back( '<' );
         }
      }
      else if ( ( source.mY == 0 ) && ( target.mX == 3 ) )
      {
         // if we are going from the left column to the bottom row, go right first then down to avoid the empty space
         for ( int j = 0; j < yDiff; j++ )
         {
            returnSequence.push_back( '>' );
         }
         for ( int j = 0; j < xDiff; j++ )
         {
            returnSequence.push_back( 'v' );
         }
      }
      else
      {
         if ( yDiff < 0 )
         {
            for ( int j = 0; j < -yDiff; j++ )
            {
               returnSequence.push_back( '<' );
            }
         }
         if ( xDiff > 0 )
         {
            for ( int j = 0; j < xDiff; j++ )
            {
               returnSequence.push_back( 'v' );
            }
         }
         if ( xDiff < 0 )
         {
            for ( int j = 0; j < -xDiff; j++ )
            {
               returnSequence.push_back( '^' );
            }
         }
         if ( yDiff > 0 )
         {
            for ( int j = 0; j < yDiff; j++ )
            {
               returnSequence.push_back( '>' );
            }
         }
      }
      // press the "A" key at the end
      returnSequence.push_back( 'A' );
      current = aSequence[i];
   }
   return returnSequence;
}

/**
 * @brief Recursive funtion. Calculate the number of keys that will have to be typed on the aRecursiveDepth keypad to get the
 *        robot operating the aRecursiveDepth - 1 keypad to type the given sequence of keys. uses memoization for optimization.
 *
 * @param aSequence a sequence of keys to type on the aRecursiveDepth - 1 keypad
 * @param aLookupTable a lookup table of keys to type to go from one key to another on the aRecursiveDepth - 1 keypad
 * @param aMaxRecursiveDepth the number of intermediate keypads between us and the robot typing on the numerical keypad
 * @param aRecursiveDepth the current recurive depth
 * @param aCache a cache memory of sequence/recursive depth to number of keys to type
 * @return the number of keys to type at a given recursive depth to type the given sequence at a recurve depth - 1
 */
int64_t directionalKeypad( const std::string                              &aSequence,
                           std::map<std::string, std::string>             &aLookupTable,
                           const int                                      aMaxRecursiveDepth,
                           const int                                      aRecursiveDepth,
                           std::map<std::pair<std::string, int>, int64_t> &aCache )
{
   // if we have already determined the number of keys to type, don't calculate it again
   if ( aCache.contains( std::make_pair( aSequence, aRecursiveDepth ) ) )
   {
      return aCache[std::make_pair( aSequence, aRecursiveDepth )];
   }
   // if we have reached the max recursive depth, return the length of the sequence
   if ( ( aRecursiveDepth >= aMaxRecursiveDepth ) || ( aSequence == "A" ) )
   {
      return aSequence.size();
   }
   // else, calculate the number of keys to type
   int64_t size        = 0;
   std::string current = "A"; // start from key "A"
   for ( int i = 0; i < aSequence.size(); i++ )
   {
      size   += directionalKeypad( aLookupTable[current + aSequence[i]], aLookupTable, aMaxRecursiveDepth, aRecursiveDepth + 1, aCache );
      current = aSequence[i];
   }
   // update the cache memory
   aCache[std::make_pair( aSequence, aRecursiveDepth )] = size;
   return size;
}

/**
 * @brief Calculate the number of keys to type on our directional keypad to get the robot operating the
 *        numerical keypad to type the given sequence of numbers.
 *
 * @param aInputFilePath the input file
 * @param aRobotsCount the number of intermediary robots between us and the numerical keypad
 * @return int64_t the number of keys to type on our directional keypad
 */
int64_t compute( const std::string aInputFilePath, const int aRobotsCount )
{
   int64_t sum = 0;

   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      std::regex  numReg( R"(\d+)" );
      std::smatch numMatch;
      std::map<std::pair<std::string, int>, int64_t> cache; // cache momory for memoization
      while ( std::getline( inputFile, line ) )
      {
         regex_search( line, numMatch, numReg );
         int code                  = std::stoi( numMatch[0] );
         std::string firstSequence = numericKeypad( line );
         sum += code * directionalKeypad( firstSequence, directionalKeypadLookupTable, aRobotsCount, 0, cache );
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
      printf( "Part 1 solution: %ld\n", compute( argv[1], 2 ) );
      printf( "Part 2 solution: %ld\n", compute( argv[1], 25 ) );
   }
   return 0;
}
