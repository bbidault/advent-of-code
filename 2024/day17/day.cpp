// https://adventofcode.com/2024/day/17

#include <cassert>
#include <fstream>
#include <regex>
#include <vector>

/**
 * @brief the computer register
 */
struct Register
{
   int64_t mA = 0;
   int64_t mB = 0;
   int64_t mC = 0;

   /**
    * @brief Register constructor
    *
    * @param aA a A register value
    * @param aB a B register value
    * @param aC a C register value
    */
   Register( const int64_t aA, const int64_t aB, const int64_t aC )
   {
      mA = aA;
      mB = aB;
      mC = aC;
   }
};

/**
 * @brief Get the combo value of a given operrand
 *
 * @param aOperrand a operrand
 * @param aRegister the computer register
 * @return int64_t the combo value of a given operrand
 */
int64_t combo( const int aOperrand, const Register &aRegister )
{
   switch ( aOperrand )
   {
      case 0:
      case 1:
      case 2:
      case 3:
      {
         return aOperrand;
      }
      case 4:
      {
         return aRegister.mA;
      }
      case 5:
      {
         return aRegister.mB;
      }
      case 6:
      {
         return aRegister.mC;
      }
      case 7:
      default:
      {
         assert( false );
      }
   }
}

/**
 * @brief Run the given program for the given initial register.
 *
 * @param aProgram a program to run, defined by a vector of opcodes and operrands
 * @param aRegister the computer register
 * @return the output of the program
 */
std::vector<int> part1( const std::vector<int> &aProgram, Register &aRegister )
{
   std::vector<int> output;
   int i = 0;
   while ( i < aProgram.size() - 1 )
   {
      switch ( aProgram[i] )
      {
         case 0:
         {
            aRegister.mA = aRegister.mA >> combo( aProgram[i + 1], aRegister );
            break;
         }
         case 1:
         {
            aRegister.mB = aRegister.mB ^ aProgram[i + 1];
            break;
         }
         case 2:
         {
            aRegister.mB = combo( aProgram[i + 1], aRegister ) % 8;
            break;
         }
         case 3:
         {
            if ( aRegister.mA != 0 )
            {
               i = aProgram[i + 1] - 2;
            }
            break;
         }
         case 4:
         {
            aRegister.mB = aRegister.mB ^ aRegister.mC;
            break;
         }
         case 5:
         {
            output.push_back( combo( aProgram[i + 1], aRegister ) % 8 );
            break;
         }
         case 6:
         {
            aRegister.mB = aRegister.mA >> combo( aProgram[i + 1], aRegister );
            break;
         }
         case 7:
         {
            aRegister.mC = aRegister.mA >> combo( aProgram[i + 1], aRegister );
            break;
         }
         default:
         {
            assert( false );
            break;
         }
      }
      i += 2;
   }
   return output;
}

/**
 * @brief Calculates the value of register A that would lead the given program to output a copy of the program.
 *
 * @note This function is build on the assumption that
 *          - the one before last instruction of the program divides the A register value by 8
 *          - the last instruction of the program leads to the program to loop back to the beginning if the A
 *            register value is not 0
 *          - there are no over jump bevaviors defines in the program
 *          - the value of register B and C do not depend on the values of the same registers from the prior loop call
 *       This function could run indefinitely if there is no valid solution or the candidate A register value overflows.
 *
 * @param aProgram a program to run, defined by a vector of opcodes and operrands
 * @return int64_t the value of register A that would lead the given program to output a copy of the program
 */
int64_t part2( const std::vector<int> &aProgram )
{
   int64_t k = 1; // multiple of 8
   while ( true )
   {
      int64_t i = 0;
      while ( true )
      {
         Register reg( k + i, 0, 0 );
         std::vector<int> res = part1( aProgram, reg );
         // the most significant bits of the answer will impact the end of the output, we need to find a solution
         // that outputs a copy of the end of the solution, and work our way backward along the program definition
         std::vector<int> ans( aProgram.begin() + aProgram.size() - res.size(), aProgram.end() );
         if ( res == ans )
         {
            if ( res.size() == aProgram.size() ) // if the solution and answer are equal, we are done
            {
               return k + i;
            }
            k = ( k + i ) * 8;
            break;
         }
         i++;
      }
   }
   return 0;
}

/**
 * @brief For part 1, run the given program for the given initial register, for part 2, calculate the value
 *        of register A that would lead the given program to output a copy of the program.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 */
void compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::ifstream inputFile( aInputFilePath );

   if ( inputFile.is_open() )
   {
      // parse the input
      std::string line = "";
      Register    reg( 0, 0, 0 );
      std::vector<int> program;
      std::regex  numReg( R"(\d+)" );
      std::smatch numMatch;
      std::getline( inputFile, line );
      regex_search( line, numMatch, numReg );
      reg.mA = std::stoi( numMatch[0] );
      std::getline( inputFile, line );
      regex_search( line, numMatch, numReg );
      reg.mB = std::stoi( numMatch[0] );
      std::getline( inputFile, line );
      regex_search( line, numMatch, numReg );
      reg.mC = std::stoi( numMatch[0] );
      std::getline( inputFile, line ); // empty line
      std::getline( inputFile, line );
      std::string::const_iterator numSearchStart( line.cbegin() );
      while ( regex_search( numSearchStart, line.cend(), numMatch, numReg ) )
      {
         program.push_back( std::stoi( numMatch[0] ) );
         numSearchStart = numMatch.suffix().first;
      }

      if ( aPart1 )
      {
         std::vector<int> output = part1( program, reg );
         for ( int i = 0; i < output.size(); i++ )
         {
            printf( "%d,", output[i] );
         }
         printf( "\n" );
      }
      else
      {
         printf( "%ld\n", part2( program ) );
      }

      inputFile.close();
   }
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
      printf( "Part 1 solution: " );
      compute( argv[1], true );
      printf( "Part 2 solution: " );
      compute( argv[1], false );
   }
   return 0;
}
