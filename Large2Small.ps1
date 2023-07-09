# Set the maximum size of the output pcap files, in MB
$max_size = 1/250
$max_files = 5
$SOURCE_PCAP_DIR = "1_Pcap"
# Iterate over the pcap files in the current directory
#foreach ($file in Get-ChildItem *.pcap)

$OUTPUT_DIR = "2_Splitted/"
if (!(Test-Path -Path $OUTPUT_DIR)){
    New-Item -ItemType Directory -Path $OUTPUT_DIR
}
if (!(Test-Path -Path "$OUTPUT_DIR/")){
    New-Item -ItemType Directory -Path "$OUTPUT_DIR/"
}
foreach ($file in Get-ChildItem $SOURCE_PCAP_DIR)
{
    # Create a subfolder for the output pcap files
    $output_folder = "$OUTPUT_DIR/$($file.Basename)"
    New-Item -ItemType Directory -Path $output_folder | Out-Null

    # Set the base file name for the output files
    $output_file = "$output_folder/$($file.Basename).pcap"

    # Split the pcap file into smaller files with a maximum size of $max_size MB
    editcap -c $($max_size*100000) $file $output_file
}









