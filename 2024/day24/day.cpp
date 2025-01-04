// https://adventofcode.com/2024/day/24

#include <fstream>
#include <map>
#include <vector>

/**
 * @brief a gate, defined by two inputs, a logic gate and one output
 */
struct Gate
{
   std::string mInput1;
   std::string mInput2;
   std::string mOperator;
   std::string mOutput;

   /**
    * @brief a Gate default constructor
    */
   Gate()
   {
      mInput1   = "";
      mInput2   = "";
      mOperator = "";
      mOutput   = "";
   }

   /**
    * @brief a Gate constructor from parameters
    *
    * @param aInput1 an input wire
    * @param aInput2 a second input wire
    * @param aOperator a logic gate operator
    * @param aOutput an output wire
    */
   Gate( const std::string &aInput1,
         const std::string &aInput2,
         const std::string &aOperator,
         const std::string &aOutput )
   {
      mInput1   = aInput1;
      mInput2   = aInput2;
      mOperator = aOperator;
      mOutput   = aOutput;
   }
};

/**
 * @brief Get the decimal output of a binary machine defined by a set of logic gates and wires
 *
 * @param aWires a vector of wires connecting logic gates
 * @param aGates a vector of logic gates
 * @return int64_t the decimal output of the machine
 */
int64_t getResult( std::map<std::string, int> &aWires, const std::vector<Gate> &aGates )
{
   // loop through all the gates until all the output wires are set to either 0 or 1
   bool outputIncomplete = true;
   while ( outputIncomplete )
   {
      outputIncomplete = false;
      for ( int i = 0; i < aGates.size(); i++ )
      {
         if ( aWires[aGates[i].mOutput] == -1 )
         {
            if ( ( aWires[aGates[i].mInput1] != -1 ) && ( aWires[aGates[i].mInput2] != -1 ) )
            {
               if ( aGates[i].mOperator == "AND" )
               {
                  aWires[aGates[i].mOutput] = aWires[aGates[i].mInput1] && aWires[aGates[i].mInput2];
               }
               else if ( aGates[i].mOperator == "OR" )
               {
                  aWires[aGates[i].mOutput] = aWires[aGates[i].mInput1] || aWires[aGates[i].mInput2];
               }
               else if ( aGates[i].mOperator == "XOR" )
               {
                  aWires[aGates[i].mOutput] = aWires[aGates[i].mInput1] ^ aWires[aGates[i].mInput2];
               }
            }
            else
            {
               outputIncomplete = true;
            }
         }
      }
   }
   // form the output binary number from the output wires values
   std::map<std::string, int>::iterator wire_itr = std::prev( aWires.end() );
   std::string binary;
   for (; wire_itr != aWires.begin(); wire_itr-- )
   {
      if ( wire_itr->first[0] == 'z' )
      {
         binary += std::to_string( wire_itr->second );
      }
      else
      {
         break;
      }
   }
   // connvert to decimal
   return std::stol( binary, nullptr, 2 );
}

/**
 * @brief Get the expected result assuming the machine is a binary adder.
 *
 * @param aWires a vector of wires connecting logic gates
 * @return the expected result of the machine
 */
int64_t getExpectedResult( std::map<std::string, int> &aWires )
{
   std::string binaryX = "";
   std::string binaryY = "";
   for ( int i = 45; i >= 0; i-- )
   {
      std::string wireX = "x";
      std::string wireY = "y";
      if ( i < 10 )
      {
         wireX += "0";
         wireY += "0";
      }
      wireX   += std::to_string( i );
      wireY   += std::to_string( i );
      binaryX += std::to_string( aWires[wireX] );
      binaryY += std::to_string( aWires[wireY] );
   }
   // connvert to decimal and add
   return std::stol( binaryX, nullptr, 2 ) + std::stol( binaryY, nullptr, 2 );
}

/**
 * @brief Print a single gate. Recursively call the function on the inputs of the gate of interest.
 *
 * @param aGates a vector of logic gates connected by logic gates
 * @param aOutput the output wire of the gate of interest
 */
void printGate( std::vector<Gate> &aGates, const std::string &aOutput )
{
   for ( int i = 0; i < aGates.size(); i++ )
   {
      if ( aGates[i].mOutput == aOutput )
      {
         std::string input1 = aGates[i].mInput1;
         std::string input2 = aGates[i].mInput2;
         printf( "%s = %s %s %s\n", aGates[i].mOutput.c_str(), input1.c_str(), aGates[i].mOperator.c_str(), input2.c_str() );
         // erase this gate to only print gates that have not been printed yet
         aGates.erase( aGates.begin() + i );
         // recursive call on the gate's inputs
         printGate( aGates, input1 );
         printGate( aGates, input2 );
      }
   }
}

/**
 * @brief Print the machine gates.
 *
 * @param aGates a vector of logic gates
 */
void printMachine( std::vector<Gate> aGates )
{
   for ( int i = 0; i < 46; i++ )
   {
      std::string out = "z";
      if ( i < 10 )
      {
         out += "0";
      }
      out += std::to_string( i );
      printGate( aGates, out );
      printf( "\n" );
   }
}

/**
 * @brief For part 1, get the decimal output of a binary machine defined by a set of logic gates and wires.
 *        For part 2, print the machine and verify that it is properly setup as a binary adder.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 */
void compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::map<std::string, int> wires;
      std::vector<Gate> gates;
      // parse the input file
      std::string line    = "";
      bool parseInitValue = true;
      while ( std::getline( inputFile, line ) )
      {
         if ( line.empty() )
         {
            parseInitValue = false;
         }
         else if ( parseInitValue )
         {
            wires[line.substr( 0, 3 )] = line[5] - '0';
         }
         else
         {
            Gate gate;
            if ( line.size() == 17 )
            {
               gate = Gate( line.substr( 0, 3 ), line.substr( 7, 3 ), "OR", line.substr( 14, 3 ) );
            }
            else
            {
               gate = Gate( line.substr( 0, 3 ), line.substr( 8, 3 ), line.substr( 4, 3 ), line.substr( 15, 3 ) );
            }
            if ( false == wires.contains( gate.mInput1 ) )
            {
               wires[gate.mInput1] = -1;
            }
            if ( false == wires.contains( gate.mInput2 ) )
            {
               wires[gate.mInput2] = -1;
            }
            if ( false == wires.contains( gate.mOutput ) )
            {
               wires[gate.mOutput] = -1;
            }
            gates.push_back( gate );
         }
      }
      inputFile.close();
      if ( aPart1 )
      {
         printf( "%ld\n", getResult( wires, gates ) );
      }
      else
      {
         // The machine is a binary adder
         // if the machine is properly setup, z00 should be calculated the following way
         // z00 = y00 XOR x00

         // if the machine is properly setup, z01 should be calculated the following way, c is the carry
         // aaa = y01 XOR x01
         // c00 = x00 AND y00
         // z01 = aaa XOR c00

         // finally, if the machine is properly setup, z(n+1) should be calculated the following way
         // c01 = x01 AND y01
         // bbb = aaa AND c00
         // ccc = bbb OR c01
         // ddd = x(n+1) XOR y(n+1)
         // z(n+1) = ccc XOR ddd

         // we print the machine gates and visualy verify that the machine follows the rules
         // defined above, making corrections as needed and keeping track of the necessary
         // changes (the solution)
         printMachine( gates );
         // we can also compare the result outputed by the machine against the expected result
         if ( getResult( wires, gates ) == getExpectedResult( wires ) )
         {
            printf( "The machine is fixed! :)\n" );
         }
         else
         {
            printf( "The machine is broken. :(\n" );
         }
      }
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
      printf( "Part 2 solution:\n" );
      compute( argv[1], false );
   }
   return 0;
}
