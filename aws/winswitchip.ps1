# current node change that own ip 
$old_ips = (Invoke-RestMethod http://169.254.169.254/latest/meta-data/public-ipv4)
echo $old_ips >> oldip.txt
$eid  = (Invoke-RestMethod http://169.254.169.254/latest/meta-data/instance-id)


$newip = aws ec2 allocate-address --domain vpc --query "PublicIp" --output text
$newstreamreader = New-Object System.IO.StreamReader("oldip.txt")
while (($readeachline = $newstreamreader.ReadLine()) -ne $null)
{
        if( $readeachline = $newip){
            aws ec2 disassociate-address --public-ip $old_ips 2> $null
            if( $? -ne 0 ) {
                aws ec2 release-address --allocation-id $(aws ec2 describe-addresses --filters "Name=public-ip,Values=$old_ips" --query "Addresses[*].[AllocationId]" --output text)
            }else {
               aws ec2 associate-address --instance-id $eid  --public-ip $newip
               break
            }

         }else {
            aws ec2 associate-address --instance-id $eid  --public-ip $newip
            break
         }
}

$newstreamreader.Dispose()
